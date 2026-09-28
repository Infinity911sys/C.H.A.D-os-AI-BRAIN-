from __future__ import annotations

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
import json

from chad_os.runtime.bootstrap import ChadOSApplication


class ApplicationServer(ThreadingHTTPServer):
    def __init__(self, server_address: tuple[str, int], app: ChadOSApplication) -> None:
        super().__init__(server_address, RequestHandler)
        self.app = app


class RequestHandler(BaseHTTPRequestHandler):
    server: ApplicationServer

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json_body(self) -> dict[str, Any]:
        length = int(self.headers.get('Content-Length', '0'))
        raw = self.rfile.read(length) if length else b'{}'
        return json.loads(raw or b'{}')

    def _is_authorized(self) -> bool:
        headers = {key: value for key, value in self.headers.items()}
        return self.server.app.identity.authorize(headers)

    def _require_auth(self) -> bool:
        if self.path == '/healthz':
            return True
        if self._is_authorized():
            return True
        self._send_json(HTTPStatus.UNAUTHORIZED, {'error': 'unauthorized'})
        return False

    def do_GET(self) -> None:
        if not self._require_auth():
            return
        if self.path == '/healthz':
            self._send_json(HTTPStatus.OK, self.server.app.health())
            return
        if self.path == '/v1/dashboard':
            self._send_json(HTTPStatus.OK, self.server.app.dashboard.snapshot())
            return
        if self.path == '/v1/registry/core':
            self._send_json(HTTPStatus.OK, {'systems': self.server.app.registry.core_systems()})
            return
        self._send_json(HTTPStatus.NOT_FOUND, {'error': 'not found'})

    def do_POST(self) -> None:
        if not self._require_auth():
            return
        body = self._json_body()
        if self.path == '/v1/telemetry':
            self._send_json(HTTPStatus.OK, self.server.app.ingest_telemetry(body))
            return
        if self.path == '/v1/control/dispatch':
            self._send_json(HTTPStatus.OK, self.server.app.dispatch_incident(body))
            return
        self._send_json(HTTPStatus.NOT_FOUND, {'error': 'not found'})

    def log_message(self, format: str, *args: Any) -> None:
        return
