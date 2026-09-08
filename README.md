# AutoFalloutShelter

Automated gameplay system for Fallout Shelter — computer vision, dynamic dweller
tracking, and vault strategy.

## Current status (verified)

Steam login from this cloud environment is **blocked**, so live game control is
unavailable here. Work continues on a verified stack that:

1. Detects dwellers on **real vault screenshots** from prior play sessions
2. Tracks them dynamically with multi-object IDs + velocity prediction
3. Plays a **dynamic vault simulator** to a win condition (population + happiness + resources)

```bash
PYTHONPATH=. python main.py --mode sim-win
PYTHONPATH=. python main.py --mode probe --screenshot assets/screenshots/vault_now.png
PYTHONPATH=. python -m pytest tests/ -v
```

## What was wrong with the old stubs

The original `src/*` modules were empty TODOs. They are **not** assumed correct.
Detection/tracking were rebuilt and tested against real frames in
`assets/screenshots/` plus the simulator in `src/sim/`.

## Dynamic dweller tracking

Dwellers walk continuously — static hover grids fail. The tracker:

- Detects vault-suit blobs (blue jumpsuit + yellow band), clothing color, and motion
- Suppresses lime collect-icons that fake person detections
- Associates detections to tracks with distance + appearance + velocity EMA
- Keeps IDs across short misses / jitter

Core code: `src/vision/dweller_detect.py`, `src/vision/dweller_tracker.py`.

## Live game (when Steam works again)

`--mode live` is intentionally disabled until a Fallout Shelter window is
available. Prior Windows bot code (`realtime_tracker.py`, `vault_pace.py`) lives
in the operator Drive folder and can be ported onto this Linux CV core.

### HITL login (required)

**Any authentication / login that needs a human must stay HITL.** Do not automate
Steam QR, account passwords, 2FA, captchas, or other sign-in flows. Present the
login UI (or pause) and wait for the operator to complete it. Automating login
has already triggered Steam endpoint blocks in this environment.

## Disclaimer

Educational use. Respect the game's terms of service.
