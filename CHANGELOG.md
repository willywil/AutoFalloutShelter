# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Verified vault-suit dweller detector + multi-object tracker (`src/vision/dweller_detect.py`, `dweller_tracker.py`)
- Dynamic vault simulator with ground-truth dwellers (`src/sim/vault_sim.py`)
- Play-to-win strategy loop for the simulator (`src/strategy/play.py`)
- Real vault screenshot corpus under `assets/screenshots/` for CV regression
- Pytest suite covering real-frame detection, ID persistence, and sim win

### Changed
- `main.py` defaults to `--mode sim-win` (Steam login blocked in cloud env)
- Stub vision/strategy APIs now raise or delegate to verified code instead of silent `pass`

### Notes
- Live Fallout Shelter via Steam is unavailable here (login endpoints blocked)
- Prior Windows operator bot (`realtime_tracker.py` / `vault_pace.py`) remains reference in Drive

---

## Project Status

**Current Phase**: Verified CV foundation + simulator play loop

### Next Milestones

1. Reconnect live game when Steam/auth path works
2. Port Windows input layer onto Linux X11 for real vault control
3. Improve MOT recall on crowded rooms / door queues
