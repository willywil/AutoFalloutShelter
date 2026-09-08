"""Dweller detection and track datatypes."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Detection:
    """Single-frame person-like detection."""

    cx: float
    cy: float
    w: float
    h: float
    score: float
    source: str = "suit"  # suit | color | motion

    @property
    def as_int(self) -> tuple[int, int]:
        return int(round(self.cx)), int(round(self.cy))

    def to_json(self) -> dict[str, Any]:
        return {
            "cx": round(self.cx, 1),
            "cy": round(self.cy, 1),
            "w": round(self.w, 1),
            "h": round(self.h, 1),
            "score": round(self.score, 3),
            "source": self.source,
        }


@dataclass
class Track:
    """Persistent multi-frame dweller identity with velocity."""

    tid: int
    cx: float
    cy: float
    vx: float = 0.0
    vy: float = 0.0
    w: float = 24.0
    h: float = 48.0
    hits: int = 1
    age: int = 1
    missed: int = 0
    zone: str = "unknown"
    last_ts: float = 0.0
    appearance: tuple[float, float, float] = (0.0, 0.0, 0.0)
    history: list[tuple[float, float]] = field(default_factory=list)

    def predict(self, dt: float) -> tuple[float, float]:
        return self.cx + self.vx * dt, self.cy + self.vy * dt

    def as_int(self) -> tuple[int, int]:
        return int(round(self.cx)), int(round(self.cy))

    def to_json(self) -> dict[str, Any]:
        return {
            "tid": self.tid,
            "cx": round(self.cx, 1),
            "cy": round(self.cy, 1),
            "vx": round(self.vx, 2),
            "vy": round(self.vy, 2),
            "w": round(self.w, 1),
            "h": round(self.h, 1),
            "hits": self.hits,
            "missed": self.missed,
            "zone": self.zone,
        }


@dataclass
class TrackSnapshot:
    """Frame-level tracker output for evaluation."""

    frame_index: int
    timestamp: float
    tracks: list[Track]
    detections: list[Detection]

    @property
    def active_count(self) -> int:
        return sum(1 for t in self.tracks if t.missed == 0)
