"""Verify dynamic tracking + play-to-win on the vault simulator."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from src.sim.vault_sim import VaultSim, VaultSimConfig
from src.strategy.play import play_to_win
from src.vision.dweller_tracker import DwellerTracker

ART = Path(__file__).resolve().parents[1] / "artifacts"
ART.mkdir(exist_ok=True)


def _match_rate(tracks, truth, dist=40.0) -> float:
    if not truth:
        return 0.0
    used = set()
    hits = 0
    for gt in truth:
        best_i, best_d = -1, dist
        for i, tr in enumerate(tracks):
            if i in used or tr.missed > 0:
                continue
            d = ((tr.cx - gt["cx"]) ** 2 + (tr.cy - gt["cy"]) ** 2) ** 0.5
            if d < best_d:
                best_d, best_i = d, i
        if best_i >= 0:
            used.add(best_i)
            hits += 1
    return hits / len(truth)


def test_sim_tracker_maintains_identity_under_motion():
    sim = VaultSim(VaultSimConfig(n_dwellers=10, seed=7, width=960, height=540))
    tracker = DwellerTracker()
    # Warm-up
    for i in range(5):
        sim.step(1 / 12)
        tracker.update(sim.render(), ts=i * 0.08)

    # Map ground-truth sid -> track id after warm-up
    snap = tracker.update(sim.render(), ts=0.5)
    truth = sim.ground_truth()
    sid_to_tid = {}
    used = set()
    for gt in truth:
        best = None
        best_d = 45.0
        for tr in snap.tracks:
            if tr.tid in used or tr.missed > 0:
                continue
            d = ((tr.cx - gt["cx"]) ** 2 + (tr.cy - gt["cy"]) ** 2) ** 0.5
            if d < best_d:
                best_d = d
                best = tr
        if best is not None:
            sid_to_tid[gt["sid"]] = best.tid
            used.add(best.tid)

    assert len(sid_to_tid) >= 4, f"poor initial association {sid_to_tid}"

    # Run motion and check ID persistence for associated dwellers.
    # Move a few at a time — mass teleport every frame is unrealistic and
    # breaks any online tracker (same as real game: dwellers walk).
    persist_hits = 0
    persist_total = 0
    rates = []
    movers = list(sid_to_tid.keys())[:4]
    for i in range(50):
        sim.step(1 / 12)
        if i % 12 == 0:
            for j, sid in enumerate(movers):
                room = sim.rooms[(j + i // 12) % len(sim.rooms)]
                sim.assign(sid, room.name)
        frame = sim.render()
        snap = tracker.update(frame, ts=1.0 + i * 0.08)
        rates.append(_match_rate(snap.tracks, sim.ground_truth(), dist=55.0))
        by_tid = {t.tid: t for t in snap.tracks if t.missed <= 3}
        for sid, tid in sid_to_tid.items():
            persist_total += 1
            gt = next(g for g in sim.ground_truth() if g["sid"] == sid)
            tr = by_tid.get(tid)
            if tr is not None:
                dist = ((tr.cx - gt["cx"]) ** 2 + (tr.cy - gt["cy"]) ** 2) ** 0.5
                if dist < 90:
                    persist_hits += 1

    persist = persist_hits / max(1, persist_total)
    mean_match = float(np.mean(rates))
    dbg = tracker.annotate(sim.render(), snap)
    cv2.imwrite(str(ART / "sim_tracks.png"), dbg)
    assert mean_match >= 0.40, f"detection-truth match too low: {mean_match:.2f}"
    assert persist >= 0.30, f"ID persistence too low: {persist:.2f}"


def test_play_to_win_on_simulator():
    sim = VaultSim(
        VaultSimConfig(
            n_dwellers=10,
            win_population=16,
            win_happiness=0.55,
            seed=3,
        )
    )
    tracker = DwellerTracker()

    def provider(frame):
        snap = tracker.update(frame)
        return snap.tracks

    result = play_to_win(sim, max_steps=600, tracks_provider=provider)
    cv2.imwrite(str(ART / "sim_final.png"), sim.render())
    (ART / "sim_play.json").write_text(
        __import__("json").dumps(
            {
                "won": result.won,
                "steps": result.steps,
                "final": result.final_status,
                "log_tail": result.log[-20:],
            },
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )
    assert result.won, f"did not win: {result.final_status}"
    assert result.final_status["population"] >= 16
