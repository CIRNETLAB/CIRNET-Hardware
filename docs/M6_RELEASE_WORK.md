# M6 product version work

Date: 2026-10-27. This is current work-unit evidence, separate from historical migration reports.

Hardware product remains exactly 0.1.1. Contracts and Simulator exact dependencies, artifact verification scripts, installed-resource tests, selected wheel checks, CI and current documentation now select 0.1.1. DEV remains 1.0.0a1. RPC 2.0, NCAP, firmware/protocol/register-map versions, lifecycle and unavailable physical capabilities are unchanged. Historical M4 evidence remains intact.

Changed Python/JSON/TOML syntax checks PASS. Installed-artifact/real-loopback/spawn/Stop-reset/quarantine acceptance is NOT_RUN in this work unit until committed dependency artifacts are rebuilt. No shared API environment installations were performed.

Follow README locked/offline bootstrap, build wheel/sdist to an allocator-owned external output, force-install `netcircuit_hardware_service-0.1.1-py3-none-any.whl`, run `pip check` and `scripts/check_installed.py --wheel ABSOLUTE_WHEEL`, then external-CWD `python -I -B -m pytest ABSOLUTE_TESTS --basetemp ABSOLUTE_SESSION/pytest`. Remote owns integrated API quarantine/lifecycle coverage.

All generated regression fixtures/archives used the shared external allocator session with all six Git roots. Shared-session cleanup remains with the migration owner. No stage/commit/merge/push was performed by this work unit.
