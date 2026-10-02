"""No-cache + live reload for the local preview servers of 3kutok.

HTML responses get a small script that polls ``/__livereload`` and reloads the
top-level page as soon as any file in the project changes. Pages inside
iframes (wireframes, IA) never reload on their own: the parent page reloads
and restores its scroll position and the selected wireframe from the URL.
"""

import json
import os
import threading
import time
from pathlib import Path

ENDPOINT = "/__livereload"
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".vercel"}

NO_CACHE_HEADERS = (
    ("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0"),
    ("Pragma", "no-cache"),
    ("Expires", "0"),
)

CLIENT_SCRIPT = """
<script>
(function () {
  if (window.top !== window) return;
  var KEY = "livereload-scroll:" + location.pathname + location.search;
  try {
    var saved = sessionStorage.getItem(KEY);
    if (saved !== null) {
      sessionStorage.removeItem(KEY);
      var y = Number(saved);
      addEventListener("load", function () { scrollTo(0, y); });
    }
  } catch (e) {}
  var version = null;
  function poll() {
    fetch("%(endpoint)s", { cache: "no-store" })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (version !== null && data.v !== version) {
          try { sessionStorage.setItem(KEY, String(scrollY)); } catch (e) {}
          location.reload();
          return;
        }
        version = data.v;
        setTimeout(poll, 600);
      })
      .catch(function () { setTimeout(poll, 2000); });
  }
  poll();
})();
</script>
""".replace("%(endpoint)s", ENDPOINT).encode()


class Watcher:
    """Cheap mtime fingerprint of a directory tree, cached for a short time."""

    def __init__(self, root, ttl=0.3):
        self.root = Path(root)
        self.ttl = ttl
        self._lock = threading.Lock()
        self._stamp = 0.0
        self._value = ""

    def version(self):
        with self._lock:
            now = time.monotonic()
            if now - self._stamp > self.ttl:
                self._value = self._scan()
                self._stamp = now
            return self._value

    def _scan(self):
        newest, count = 0, 0
        for dirpath, dirnames, filenames in os.walk(self.root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for name in filenames:
                try:
                    mtime = os.stat(os.path.join(dirpath, name)).st_mtime_ns
                except OSError:
                    continue
                newest = max(newest, mtime)
                count += 1
        return f"{newest}-{count}"


def inject(html_bytes):
    marker = html_bytes.lower().rfind(b"</body>")
    if marker == -1:
        return html_bytes + CLIENT_SCRIPT
    return html_bytes[:marker] + CLIENT_SCRIPT + html_bytes[marker:]


class LiveReloadMixin:
    """Mix into a SimpleHTTPRequestHandler subclass.

    ``live_reload_applies(fs_path)`` decides which files get the script and
    ``live_reload_watcher`` is the Watcher for the project tree.
    """

    live_reload_watcher = None

    def live_reload_applies(self, fs_path):
        return True

    def end_headers(self):
        for key, value in NO_CACHE_HEADERS:
            self.send_header(key, value)
        super().end_headers()

    def send_head(self):
        # Ignore conditional requests so the browser always gets fresh bytes.
        del self.headers["If-Modified-Since"]
        del self.headers["If-None-Match"]

        if self.path.split("?", 1)[0] == ENDPOINT:
            body = json.dumps({"v": self.live_reload_watcher.version()}).encode()
            return self._send_bytes(body, "application/json")

        fs_path = self.translate_path(self.path)
        if os.path.isdir(fs_path) and self.path.split("?", 1)[0].endswith("/"):
            # "/lessons/" serves lessons/index.html: inject there too.
            for index in ("index.html", "index.htm"):
                if os.path.isfile(os.path.join(fs_path, index)):
                    fs_path = os.path.join(fs_path, index)
                    break
        if (
            fs_path.endswith((".html", ".htm"))
            and os.path.isfile(fs_path)
            and self.live_reload_applies(fs_path)
        ):
            try:
                with open(fs_path, "rb") as f:
                    body = inject(f.read())
            except OSError:
                return super().send_head()
            return self._send_bytes(body, "text/html; charset=utf-8")
        return super().send_head()

    def _send_bytes(self, body, content_type):
        import io

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        return io.BytesIO(body)
