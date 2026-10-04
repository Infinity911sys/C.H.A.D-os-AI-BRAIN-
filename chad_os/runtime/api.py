from __future__ import annotations

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
import json
from urllib.parse import urlparse

from chad_os.runtime.bootstrap import ChadOSApplication
from chad_os.runtime.site import resolve_site_asset


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
        parsed = urlparse(self.path)
        if parsed.path in {
            '/',
            '/index.html',
            '/site.css',
            '/site.js',
            '/healthz',
            '/v1/algotraj/summary',
            '/v1/algotraj/play-store',
            '/v1/public/summary',
            '/v1/public/catalog',
            '/v1/public/core',
        }:
            return True
        if self._is_authorized():
            return True
        self._send_json(HTTPStatus.UNAUTHORIZED, {'error': 'unauthorized'})
        return False

    def _send_bytes(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if not self._require_auth():
            return
        parsed = urlparse(self.path)

        asset = resolve_site_asset(parsed.path)
        if asset is not None:
            file_path, content_type = asset
            self._send_bytes(HTTPStatus.OK, file_path.read_bytes(), content_type)
            return

        if parsed.path == '/healthz':
            self._send_json(HTTPStatus.OK, self.server.app.health())
            return
        if parsed.path == '/v1/algotraj/summary':
            self._send_json(HTTPStatus.OK, self.server.app.algotraj.summary())
            return
        if parsed.path == '/v1/algotraj/play-store':
            self._send_json(
                HTTPStatus.OK,
                self.server.app.algotraj.play_store_readiness(),
            )
            return
        if parsed.path == '/v1/public/summary':
            self._send_json(HTTPStatus.OK, self.server.app.registry.public_payload())
            return
        if parsed.path == '/v1/public/catalog':
            filters = self.server.app.registry.filters_from_query(parsed.query)
            self._send_json(
                HTTPStatus.OK,
                self.server.app.registry.public_catalog(**filters),
            )
            return
        if parsed.path == '/v1/public/core':
            self._send_json(
                HTTPStatus.OK,
                {'systems': self.server.app.registry.core_systems()},
            )
            return
        if parsed.path == '/v1/dashboard':
            self._send_json(HTTPStatus.OK, self.server.app.dashboard.snapshot())
            return
        if parsed.path == '/v1/algotraj/operator/dashboard':
            self._send_json(HTTPStatus.OK, self.server.app.algotraj_dashboard())
            return
        if parsed.path == '/v1/registry/core':
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
        if self.path == '/v1/algotraj/analyze':
            self._send_json(HTTPStatus.OK, self.server.app.analyze_algotraj(body))
            return
        self._send_json(HTTPStatus.NOT_FOUND, {'error': 'not found'})

    def log_message(self, format: str, *args: Any) -> None:
        return
