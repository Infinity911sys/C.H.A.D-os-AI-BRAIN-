# C.H.A.D.-OS Phase 1 Foundation

This repository now contains a runnable Phase 1 foundation for the Austin Enterprise 125-platform portfolio.

## What is implemented
- a machine-readable registry for all 125 indexed systems
- core system contracts for the initial operating core
- a Python control-plane service with:
  - bearer-token authentication
  - telemetry ingest
  - dispatch workflow generation
  - JSONL audit logging
  - dashboard and health endpoints
- a website-ready public catalog and static landing page served from this repo
- a separate standalone website bundle that can be published independently
- tests, build commands, Docker packaging, and CI

## Repository structure
- `/chad_os` — Phase 1 runtime, kernel, governance, and service modules
- `/config/system_registry.json` — canonical 125-system registry
- `/config/core_system_contracts.json` — contracts for the initial operating core
- `/config/deployment_profiles.json` — local, staging, and production deployment settings
- `/deployment` — container and Kubernetes deployment assets
- `/build/Makefile` — lint, test, run, and serve commands
- `/site` — website-facing catalog UI assets for direct publishing or embedding
- `/website` — standalone publishable website bundle with exported JSON data
- `/tests` — automated test coverage for registry, bootstrap, and API behavior
- `/Brain`, `/Index`, `/Java` — preserved legacy reference material and prototype artifacts

## Quick start
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make -f build/Makefile test
make -f build/Makefile serve
```

Default API address: `http://127.0.0.1:8080`

Default control token: `dev-control-token`

Website catalog: `http://127.0.0.1:8080/`

Standalone website build:
```bash
make -f build/Makefile website-export
make -f build/Makefile website-serve
```

Standalone website address: `http://127.0.0.1:8090/`

## API surface
- `GET /` — public website landing page and catalog UI
- `GET /v1/public/summary` — public portfolio summary for website consumption
- `GET /v1/public/catalog` — public searchable/filterable 125-system catalog
- `GET /v1/public/core` — public initial operating-core listing
- `GET /healthz` — service health
- `GET /v1/dashboard` — authenticated portfolio and runtime dashboard
- `GET /v1/registry/core` — authenticated view of the core operating systems
- `POST /v1/telemetry` — authenticated telemetry ingest that emits a dispatch workflow
- `POST /v1/control/dispatch` — authenticated direct dispatch request

Example public catalog request:
```bash
curl "http://127.0.0.1:8080/v1/public/catalog?section=platform_core&status=partially_defined"
```

Example telemetry request:
```bash
curl -X POST http://127.0.0.1:8080/v1/telemetry   -H 'Authorization: ******'   -H 'Content-Type: application/json'   -d '{"source":"sentinel-link","severity":4,"location":"Phoenix","payload":{"incident":"fire"}}'
```

## Phase 1 scope
This implementation does **not** claim to fully operate all 125 platforms yet.
It provides the portfolio foundation requested in the plan:
- canonical inventory and classifications
- core operating contracts
- shared runtime, governance, telemetry, audit, and dashboard primitives
- one runnable vertical slice that can be extended system-by-system
- a website-ready catalog surface that can be published from this repo or integrated into a separate website repository
- a standalone website bundle with pre-exported data for separate hosting

## Validation
```bash
make -f build/Makefile lint
make -f build/Makefile test
```
