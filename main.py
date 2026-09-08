"""
Main entry for AutoFalloutShelter.

Live Steam Fallout Shelter is currently unavailable in this environment
(login endpoints blocked). Default mode runs the dynamic vault simulator
with verified dweller tracking and plays toward a win condition.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

import cv2

from src.sim import VaultSim, VaultSimConfig
from src.strategy import play_to_win
from src.utils import setup_logging
from src.vision import DwellerTracker, annotate_detections, detect_dwellers


def run_screenshot_probe(path: Path, out_dir: Path) -> dict:
    frame = cv2.imread(str(path))
    if frame is None:
        raise FileNotFoundError(path)
    dets = detect_dwellers(frame)
    tracker = DwellerTracker()
    snap = tracker.update(frame, ts=0.0)
    # Fake a few frames of identity warm-up via slight jitter
    import numpy as np

    for i in range(1, 6):
        M = np.float32([[1, 0, (i % 3) - 1], [0, 1, 0]])
        jittered = cv2.warpAffine(frame, M, (frame.shape[1], frame.shape[0]))
        snap = tracker.update(jittered, ts=i * 0.08)
    dbg = tracker.annotate(frame, snap)
    out_dir.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out_dir / f"{path.stem}_tracks.png"), dbg)
    cv2.imwrite(
        str(out_dir / f"{path.stem}_dets.png"),
        annotate_detections(frame, dets),
    )
    return {
        "image": str(path),
        "detections": len(dets),
        "tracks": tracker.summary(),
    }


def run_sim_win(out_dir: Path, *, headless: bool = True) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    sim = VaultSim(
        VaultSimConfig(
            n_dwellers=10,
            win_population=16,
            win_happiness=0.55,
            seed=3,
            width=960,
            height=540,
        )
    )
    tracker = DwellerTracker()

    def provider(frame):
        return tracker.update(frame).tracks

    result = play_to_win(sim, max_steps=700, tracks_provider=provider)
    final = sim.render()
    dbg = tracker.annotate(final)
    cv2.imwrite(str(out_dir / "sim_win_final.png"), final)
    cv2.imwrite(str(out_dir / "sim_win_tracks.png"), dbg)
    payload = {
        "won": result.won,
        "steps": result.steps,
        "final": result.final_status,
        "tracker": tracker.summary(),
        "log_tail": result.log[-30:],
    }
    (out_dir / "sim_win.json").write_text(
        json.dumps(payload, indent=2, default=str), encoding="utf-8"
    )
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="AutoFalloutShelter")
    parser.add_argument(
        "--mode",
        choices=("sim-win", "probe", "live"),
        default="sim-win",
        help="sim-win: play dynamic simulator to win; probe: analyze screenshots; live: requires game",
    )
    parser.add_argument(
        "--screenshot",
        type=Path,
        default=Path("assets/screenshots/vault_now.png"),
    )
    parser.add_argument("--out", type=Path, default=Path("artifacts"))
    args = parser.parse_args(argv)

    setup_logging()
    log = logging.getLogger("main")

    if args.mode == "live":
        log.error(
            "Live Fallout Shelter unavailable: Steam login endpoints are blocked. "
            "Use --mode sim-win or --mode probe with assets/screenshots."
        )
        return 2

    if args.mode == "probe":
        summary = run_screenshot_probe(args.screenshot, args.out)
        log.info("probe %s", json.dumps(summary, indent=2, default=str))
        print(json.dumps(summary, indent=2, default=str))
        return 0

    summary = run_sim_win(args.out)
    log.info(
        "sim-win won=%s steps=%s pop=%s hap=%s",
        summary["won"],
        summary["steps"],
        summary["final"]["population"],
        summary["final"]["happiness"],
    )
    print(json.dumps(summary, indent=2, default=str))
    return 0 if summary["won"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
