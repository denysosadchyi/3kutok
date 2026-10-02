#!/usr/bin/env python3
"""Serve the existing course site plus 3kutok on the LAN-approved port."""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

from livereload import LiveReloadMixin, Watcher


DEFAULT_ROOT = Path("/home/hp/from-den/kursy").resolve()
KOOTOK_ROOT = Path("/home/hp/3kutok").resolve()
KOOTOK_PREFIX = "/3kutok"
KOOTOK_LESSONS_PREFIX = "/lessons"


class Handler(LiveReloadMixin, SimpleHTTPRequestHandler):
    live_reload_watcher = None  # set below, after KOOTOK_ROOT

    def translate_path(self, path):
        request_path = unquote(urlsplit(path).path)
        if request_path == KOOTOK_PREFIX or request_path.startswith(KOOTOK_PREFIX + "/"):
            root = KOOTOK_ROOT
            relative = request_path[len(KOOTOK_PREFIX) :].lstrip("/")
        elif request_path == KOOTOK_LESSONS_PREFIX or request_path.startswith(
            KOOTOK_LESSONS_PREFIX + "/"
        ):
            root = KOOTOK_ROOT
            relative = request_path.lstrip("/")
        else:
            root = DEFAULT_ROOT
            relative = request_path.lstrip("/")

        candidate = (root / relative).resolve()
        if candidate == root or root in candidate.parents:
            return str(candidate)
        return str(root / "__not_found__")

    def live_reload_applies(self, fs_path):
        candidate = Path(fs_path).resolve()
        return candidate == KOOTOK_ROOT or KOOTOK_ROOT in candidate.parents


Handler.live_reload_watcher = Watcher(KOOTOK_ROOT)


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8088), Handler).serve_forever()
