""" empirically verify dweller detection on real vault screenshots."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
import pytest

from src.vision.dweller_detect import (
    annotate_detections,
    detect_dwellers,
    detect_vault_suit_blobs,
)
from src.vision.dweller_tracker import DwellerTracker

ASSETS = Path(__file__).resolve().parents[1] / "assets" / "screenshots"
ART = Path(__file__).resolve().parents[1] / "artifacts"
ART.mkdir(exist_ok=True)


def _load(name: str):
    path = ASSETS / name
    if not path.exists():
        pytest.skip(f"missing screenshot {path}")
    frame = cv2.imread(str(path))
    assert frame is not None
    return frame


def test_suit_detector_finds_dwellers_on_vault_now():
    frame = _load("vault_now.png")
    dets = detect_vault_suit_blobs(frame)
    # Real vault has ~12+ dwellers; suits alone may miss some — require a
    # meaningful count, not zero, and not exploding into icon spam.
    assert 4 <= len(dets) <= 40, f"unexpected suit count {len(dets)}"
    h, w = frame.shape[:2]
    # No detections in top HUD band
    assert all(d.cy > h * 0.14 for d in dets)
    dbg = annotate_detections(frame, dets)
    cv2.imwrite(str(ART / "test_vault_now_suits.png"), dbg)


def test_merged_detector_reasonable_on_vault_now():
    frame = _load("vault_now.png")
    dets = detect_dwellers(frame)
    assert 6 <= len(dets) <= 45, f"unexpected merged count {len(dets)}"
    # Centers should cluster in vault cross-section (not extreme corners)
    h, w = frame.shape[:2]
    mid = [d for d in dets if 0.05 * w < d.cx < 0.92 * w and 0.15 * h < d.cy < 0.80 * h]
    assert len(mid) >= 5
    dbg = annotate_detections(frame, dets)
    cv2.imwrite(str(ART / "test_vault_now_merged.png"), dbg)


def test_detector_runs_on_multiple_real_frames():
    counts = {}
    for name in ("vault_now.png", "session_end.png", "pace_now.png", "vault_for_collect.png"):
        path = ASSETS / name
        if not path.exists():
            continue
        frame = cv2.imread(str(path))
        dets = detect_dwellers(frame)
        counts[name] = len(dets)
        assert len(dets) >= 1, f"{name} produced zero detections"
    assert counts, "no screenshots available"
    (ART / "detect_counts.json").write_text(
        __import__("json").dumps(counts, indent=2), encoding="utf-8"
    )


def test_tracker_holds_ids_on_jittered_real_frame():
    """Simulate micro-motion by shifting crops — IDs should persist."""
    frame = _load("vault_now.png")
    tracker = DwellerTracker()
    # Warm-up on original
    snap0 = tracker.update(frame, ts=0.0)
    n0 = snap0.active_count
    assert n0 >= 3

    id_sets = []
    for i in range(1, 8):
        # Small affine jitter to emulate camera / dweller motion
        M = np.float32([[1, 0, (i % 3) - 1], [0, 1, (i % 2)]])
        jittered = cv2.warpAffine(frame, M, (frame.shape[1], frame.shape[0]))
        snap = tracker.update(jittered, ts=i * 0.08)
        active_ids = {t.tid for t in snap.tracks if t.missed == 0 and t.hits >= 2}
        id_sets.append(active_ids)

    # Intersection of mature IDs across jitter frames should be non-empty
    stable = set.intersection(*id_sets) if id_sets else set()
    assert len(stable) >= 1, f"no stable IDs across jitter; sets={id_sets}"
    dbg = tracker.annotate(frame, snap0)
    cv2.imwrite(str(ART / "test_vault_now_tracks.png"), dbg)
