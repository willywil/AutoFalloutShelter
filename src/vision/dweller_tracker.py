"""Dynamic multi-object dweller tracker.

Dwellers walk continuously. Static grids fail — this tracker:
  1) Detects person-like blobs each frame
  2) Associates with velocity-predicted tracks (greedy + appearance)
  3) Keeps identity across missed frames / short occlusions
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import cv2
import numpy as np

from src.models.dweller import Detection, Track, TrackSnapshot
from src.vision.dweller_detect import annotate_detections, detect_dwellers


@dataclass
class TrackerConfig:
    match_dist: float = 58.0
    max_missed: int = 10
    min_hits_to_act: int = 2
    appearance_weight: float = 0.35
    vel_ema: float = 0.65


def _zone_for(frame: np.ndarray, x: float, y: float) -> str:
    h, w = frame.shape[:2]
    if x < w * 0.28:
        return "door"
    if y > h * 0.55:
        return "living"
    return "vault"


def _mean_bgr(frame: np.ndarray, det: Detection) -> tuple[float, float, float]:
    h, w = frame.shape[:2]
    x0 = int(max(0, det.cx - det.w / 2))
    y0 = int(max(0, det.cy - det.h / 2))
    x1 = int(min(w, det.cx + det.w / 2))
    y1 = int(min(h, det.cy + det.h / 2))
    crop = frame[y0:y1, x0:x1]
    if crop.size == 0:
        return (0.0, 0.0, 0.0)
    mean = crop.reshape(-1, 3).mean(axis=0)
    return float(mean[0]), float(mean[1]), float(mean[2])


def _appearance_dist(
    a: tuple[float, float, float], b: tuple[float, float, float]
) -> float:
    return float(np.linalg.norm(np.array(a) - np.array(b)))


class DwellerTracker:
    """Online MOT for vault dwellers."""

    def __init__(self, cfg: TrackerConfig | None = None) -> None:
        self.cfg = cfg or TrackerConfig()
        self.tracks: list[Track] = []
        self._next_id = 1
        self.prev_gray: np.ndarray | None = None
        self.frame_index = 0

    def reset(self) -> None:
        self.tracks.clear()
        self._next_id = 1
        self.prev_gray = None
        self.frame_index = 0

    def update(
        self, frame: np.ndarray, ts: float | None = None
    ) -> TrackSnapshot:
        import time

        ts = ts if ts is not None else time.time()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        dets = detect_dwellers(frame, self.prev_gray)
        self.prev_gray = gray
        self.frame_index += 1

        # Predict forward
        for tr in self.tracks:
            dt = max(0.01, ts - tr.last_ts) if tr.last_ts else 0.08
            tr.cx, tr.cy = tr.predict(dt)
            tr.age += 1
            tr.missed += 1

        used: set[int] = set()
        cfg = self.cfg
        for tr in sorted(self.tracks, key=lambda t: -t.hits):
            best_i, best_cost = -1, cfg.match_dist
            for i, d in enumerate(dets):
                if i in used:
                    continue
                dist = float(np.hypot(d.cx - tr.cx, d.cy - tr.cy))
                app = _appearance_dist(tr.appearance, _mean_bgr(frame, d))
                # Normalize appearance into distance-like units
                cost = dist + cfg.appearance_weight * (app / 40.0) * cfg.match_dist
                if cost < best_cost:
                    best_cost, best_i = cost, i
            if best_i < 0:
                continue
            d = dets[best_i]
            used.add(best_i)
            dt = max(0.02, ts - tr.last_ts) if tr.last_ts else 0.08
            nx, ny = float(d.cx), float(d.cy)
            tr.vx = cfg.vel_ema * tr.vx + (1 - cfg.vel_ema) * (nx - tr.cx) / dt
            tr.vy = cfg.vel_ema * tr.vy + (1 - cfg.vel_ema) * (ny - tr.cy) / dt
            tr.cx, tr.cy = nx, ny
            tr.w, tr.h = float(d.w), float(d.h)
            tr.hits += 1
            tr.missed = 0
            tr.last_ts = ts
            tr.zone = _zone_for(frame, nx, ny)
            tr.appearance = _mean_bgr(frame, d)
            tr.history.append((nx, ny))
            if len(tr.history) > 40:
                tr.history = tr.history[-40:]

        for i, d in enumerate(dets):
            if i in used:
                continue
            self.tracks.append(
                Track(
                    tid=self._next_id,
                    cx=float(d.cx),
                    cy=float(d.cy),
                    w=float(d.w),
                    h=float(d.h),
                    last_ts=ts,
                    zone=_zone_for(frame, d.cx, d.cy),
                    appearance=_mean_bgr(frame, d),
                    history=[(float(d.cx), float(d.cy))],
                )
            )
            self._next_id += 1

        self.tracks = [t for t in self.tracks if t.missed <= cfg.max_missed]
        return TrackSnapshot(self.frame_index, ts, list(self.tracks), dets)

    def actionable(self) -> list[Track]:
        return [
            t
            for t in self.tracks
            if t.hits >= self.cfg.min_hits_to_act and t.missed <= 2
        ]

    def annotate(self, frame: np.ndarray, snap: TrackSnapshot | None = None) -> np.ndarray:
        out = frame.copy()
        tracks = snap.tracks if snap else self.tracks
        dets = snap.detections if snap else []
        if dets:
            out = annotate_detections(out, dets)
        for tr in tracks:
            color = (0, 255, 0) if tr.missed == 0 else (0, 140, 255)
            cv2.circle(out, tr.as_int(), 11, color, 2)
            cv2.putText(
                out,
                f"id{tr.tid}:{tr.zone}",
                (int(tr.cx) + 10, int(tr.cy)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                color,
                1,
                cv2.LINE_AA,
            )
            if len(tr.history) >= 2:
                pts = np.array(tr.history, dtype=np.int32).reshape(-1, 1, 2)
                cv2.polylines(out, [pts], False, color, 1, cv2.LINE_AA)
        return out

    def summary(self) -> dict[str, Any]:
        return {
            "n_tracks": len(self.tracks),
            "active": sum(1 for t in self.tracks if t.missed == 0),
            "actionable": len(self.actionable()),
            "next_id": self._next_id,
            "tracks": [t.to_json() for t in self.tracks],
        }
