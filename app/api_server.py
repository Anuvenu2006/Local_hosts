"""Local HTTP bridge between Chip's Python engine and the Magic Patterns UI."""
from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Callable, Any


class _Handler(BaseHTTPRequestHandler):
    server_version = "ChipBridge/1.0"

    def log_message(self, fmt, *args):
        return

    def _send(self, status: int, payload: Any):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send(204, {})

    def do_GET(self):
        if self.path in ("/", "/health"):
            self._send(200, {"ok": True, "service": "chip-bridge"})
            return
        if self.path == "/api/chip/snapshot":
            self._send(200, self.server.snapshot_fn())
            return
        self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/api/chip/command":
            self._send(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            result = self.server.command_fn(payload)
            self._send(200, result or {"ok": True})
        except Exception as exc:
            self._send(400, {"ok": False, "error": str(exc)})


def start_server(snapshot_fn: Callable[[], dict], command_fn: Callable[[dict], dict], host="127.0.0.1", port=8000):
    server = ThreadingHTTPServer((host, port), _Handler)
    server.snapshot_fn = snapshot_fn
    server.command_fn = command_fn
    thread = threading.Thread(target=server.serve_forever, name="chip-api", daemon=True)
    thread.start()
    print(f"🌐 CHIP UI BRIDGE: http://{host}:{port}")
    return server
