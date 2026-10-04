from __future__ import annotations

import argparse
import json

from chad_os.runtime.api import ApplicationServer
from chad_os.runtime.bootstrap import AppConfig, ChadOSApplication


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='C.H.A.D.-OS Phase 1 runtime')
    parser.add_argument('--serve', action='store_true', help='run the HTTP control plane')
    parser.add_argument('--host', default=None)
    parser.add_argument('--port', type=int, default=None)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    config = AppConfig.from_env()
    if args.host:
        config.host = args.host
    if args.port:
        config.port = args.port

    app = ChadOSApplication(config)
    app.boot()

    if args.serve:
        server = ApplicationServer((config.host, config.port), app)
        print(f'C.H.A.D.-OS Phase 1 API listening on http://{config.host}:{config.port}')
        server.serve_forever()
        return

    print('C.H.A.D.-OS Phase 1 console ready. Type exit to quit.')
    while True:
        try:
            prompt = input('You> ').strip()
        except (EOFError, KeyboardInterrupt):
            break
        if prompt.lower() in {'exit', 'quit'}:
            break
        print(json.dumps(app.process_prompt(prompt), indent=2))


if __name__ == '__main__':
    main()
