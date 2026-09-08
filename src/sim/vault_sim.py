"""Dynamic Fallout Shelter–like vault simulator with ground-truth dwellers.

Steam login is blocked in this environment. This simulator provides a moving
target for verifying detection + multi-object tracking without the live game.
Win condition: population >= goal, happiness high, resources stable.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Any

import cv2
import numpy as np


ROOM_TYPES = ("power", "diner", "water", "living", "door")


@dataclass
class SimDweller:
    sid: int  # ground-truth id
    x: float
    y: float
    target_x: float
    target_y: float
    room: str
    color_bgr: tuple[int, int, int]
    speed: float = 55.0
    happiness: float = 0.5

    def step(self, dt: float) -> None:
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.hypot(dx, dy)
        if dist < 2.0:
            return
        step = min(self.speed * dt, dist)
        self.x += dx / dist * step
        self.y += dy / dist * step


@dataclass
class SimRoom:
    name: str
    x: int
    y: int
    w: int
    h: int
    kind: str
    ready: bool = False
    staff: int = 0

    @property
    def center(self) -> tuple[int, int]:
        return self.x + self.w // 2, self.y + self.h // 2


@dataclass
class VaultSimConfig:
    width: int = 1280
    height: int = 720
    n_dwellers: int = 12
    win_population: int = 20
    win_happiness: float = 0.75
    seed: int = 13


@dataclass
class VaultSim:
    """Lightweight vault world for tracker + strategy verification."""

    cfg: VaultSimConfig = field(default_factory=VaultSimConfig)
    dwellers: list[SimDweller] = field(default_factory=list)
    rooms: list[SimRoom] = field(default_factory=list)
    power: float = 0.7
    food: float = 0.7
    water: float = 0.7
    happiness: float = 0.35
    caps: int = 400
    t: float = 0.0
    frame_i: int = 0
    _rng: random.Random = field(default_factory=random.Random)

    def __post_init__(self) -> None:
        self._rng = random.Random(self.cfg.seed)
        self._build_layout()
        self._spawn_dwellers(self.cfg.n_dwellers)

    def _build_layout(self) -> None:
        w, h = self.cfg.width, self.cfg.height
        # Three floors of rooms similar to Fallout Shelter cross-section
        floors_y = [int(h * 0.28), int(h * 0.48), int(h * 0.68)]
        rw, rh = 170, 110
        door = SimRoom("door", int(w * 0.10), floors_y[0], 120, rh, "door")
        living = SimRoom("living", int(w * 0.32), floors_y[0], rw, rh, "living")
        power = SimRoom("power", int(w * 0.52), floors_y[0], rw, rh, "power", ready=True)
        diner = SimRoom("diner", int(w * 0.32), floors_y[1], rw, rh, "diner", ready=True)
        water = SimRoom("water", int(w * 0.52), floors_y[1], rw, rh, "water")
        storage = SimRoom("storage", int(w * 0.32), floors_y[2], rw, rh, "living")
        self.rooms = [door, living, power, diner, water, storage]

    def _spawn_dwellers(self, n: int) -> None:
        palette = [
            (40, 160, 220),  # yellow-ish BGR
            (180, 90, 40),  # blue suit
            (30, 140, 200),
            (200, 100, 50),
            (50, 170, 230),
            (170, 80, 35),
        ]
        assignable = [r for r in self.rooms if r.kind != "door"]
        # Spread dwellers across rooms with fixed slots so they don't merge
        slots_per_room = 3
        for i in range(n):
            room = assignable[i % len(assignable)]
            slot = (i // len(assignable)) % slots_per_room
            jx = -35 + slot * 35 + self._rng.uniform(-4, 4)
            jy = self._rng.uniform(-8, 12)
            x = room.center[0] + jx
            y = room.center[1] + jy
            color = palette[i % len(palette)]
            d = SimDweller(
                sid=i + 1,
                x=x,
                y=y,
                target_x=x,
                target_y=y,
                room=room.name,
                color_bgr=color,
                speed=self._rng.uniform(35, 70),
                happiness=self._rng.uniform(0.2, 0.6),
            )
            self.dwellers.append(d)
            room.staff += 1

    def ground_truth(self) -> list[dict[str, Any]]:
        return [
            {
                "sid": d.sid,
                "cx": d.x,
                "cy": d.y,
                "room": d.room,
                "happiness": d.happiness,
            }
            for d in self.dwellers
        ]

    def _pick_new_target(self, d: SimDweller) -> None:
        room = self._rng.choice(self.rooms)
        d.room = room.name
        d.target_x = room.center[0] + self._rng.uniform(-45, 45)
        d.target_y = room.center[1] + self._rng.uniform(-25, 28)

    def step(self, dt: float = 1 / 12) -> None:
        self.t += dt
        self.frame_i += 1
        # Occasional retarget — dwellers are highly dynamic
        for d in self.dwellers:
            if self._rng.random() < 0.04 or (
                abs(d.x - d.target_x) < 3 and abs(d.y - d.target_y) < 3
            ):
                if self._rng.random() < 0.55:
                    self._pick_new_target(d)
            d.step(dt)

        # Economy tick
        staffed_power = sum(1 for d in self.dwellers if d.room == "power")
        staffed_food = sum(1 for d in self.dwellers if d.room == "diner")
        staffed_water = sum(1 for d in self.dwellers if d.room == "water")
        self.power = float(np.clip(self.power + (staffed_power - 1.2) * 0.01 * dt * 12, 0, 1))
        self.food = float(np.clip(self.food + (staffed_food - 1.0) * 0.01 * dt * 12, 0, 1))
        self.water = float(np.clip(self.water + (staffed_water - 1.0) * 0.01 * dt * 12, 0, 1))
        mean_h = float(np.mean([d.happiness for d in self.dwellers])) if self.dwellers else 0
        # Happiness rises when resources green and rooms staffed
        resource_ok = (self.power + self.food + self.water) / 3
        self.happiness = float(np.clip(0.7 * mean_h + 0.3 * resource_ok, 0, 1))
        for d in self.dwellers:
            d.happiness = float(
                np.clip(d.happiness + (resource_ok - 0.45) * 0.01, 0.05, 1.0)
            )

        # Ready flags
        for r in self.rooms:
            if r.kind == "power":
                r.ready = self.power > 0.55 and staffed_power > 0
            elif r.kind == "diner":
                r.ready = self.food > 0.55 and staffed_food > 0
            elif r.kind == "water":
                r.ready = self.water > 0.55 and staffed_water > 0

    def collect(self, room_name: str) -> bool:
        room = next((r for r in self.rooms if r.name == room_name), None)
        if room is None or not room.ready:
            return False
        if room.kind == "power":
            self.caps += 8
            self.power = max(0.35, self.power - 0.12)
        elif room.kind == "diner":
            self.caps += 6
            self.food = max(0.35, self.food - 0.10)
        elif room.kind == "water":
            self.caps += 6
            self.water = max(0.35, self.water - 0.10)
        room.ready = False
        return True

    def assign(self, sid: int, room_name: str) -> bool:
        d = next((x for x in self.dwellers if x.sid == sid), None)
        room = next((r for r in self.rooms if r.name == room_name), None)
        if d is None or room is None:
            return False
        d.room = room_name
        d.target_x = room.center[0] + self._rng.uniform(-30, 30)
        d.target_y = room.center[1] + self._rng.uniform(-15, 15)
        return True

    def recruit(self) -> bool:
        """Admit a door dweller — grows population toward win."""
        if len(self.dwellers) >= self.cfg.win_population + 5:
            return False
        room = next(r for r in self.rooms if r.kind == "living")
        sid = max((d.sid for d in self.dwellers), default=0) + 1
        d = SimDweller(
            sid=sid,
            x=self.cfg.width * 0.08,
            y=self.rooms[0].center[1],
            target_x=room.center[0],
            target_y=room.center[1],
            room=room.name,
            color_bgr=(180, 90, 40),
            happiness=0.45,
        )
        self.dwellers.append(d)
        return True

    def won(self) -> bool:
        return (
            len(self.dwellers) >= self.cfg.win_population
            and self.happiness >= self.cfg.win_happiness
            and min(self.power, self.food, self.water) >= 0.45
        )

    def render(self) -> np.ndarray:
        w, h = self.cfg.width, self.cfg.height
        frame = np.zeros((h, w, 3), dtype=np.uint8)
        # Rock background
        frame[:] = (28, 28, 32)
        # Sky / wasteland band
        cv2.rectangle(frame, (0, 0), (int(w * 0.28), int(h * 0.22)), (40, 110, 180), -1)
        for i in range(5):
            cv2.circle(
                frame,
                (30 + i * 40, int(h * 0.18)),
                8,
                (20, 20, 20),
                -1,
            )
        # Rooms — muted interiors (avoid vault-suit blue/yellow so detectors work)
        for r in self.rooms:
            if r.kind == "power":
                base = (55, 60, 58)
            elif r.kind == "diner":
                base = (45, 55, 70)
            elif r.kind == "water":
                base = (70, 55, 50)
            elif r.kind == "door":
                base = (42, 42, 48)
            else:
                base = (58, 58, 64)
            cv2.rectangle(frame, (r.x, r.y), (r.x + r.w, r.y + r.h), base, -1)
            cv2.rectangle(frame, (r.x, r.y), (r.x + r.w, r.y + r.h), (18, 18, 18), 2)
            if r.ready:
                cv2.rectangle(
                    frame,
                    (r.x + 4, r.y + 4),
                    (r.x + r.w - 4, r.y + r.h - 4),
                    (40, 230, 40),
                    3,
                )
                icon_c = (r.center[0], r.y + 18)
                cv2.circle(frame, icon_c, 12, (40, 255, 40), -1)
        # Elevator (orange, not suit-blue)
        ex = int(w * 0.46)
        cv2.rectangle(frame, (ex, int(h * 0.26)), (ex + 36, int(h * 0.78)), (40, 110, 210), -1)

        # HUD
        cv2.rectangle(frame, (0, 0), (w, int(h * 0.10)), (15, 15, 18), -1)
        cv2.putText(
            frame,
            f"POP {len(self.dwellers)}  HAP {int(self.happiness*100)}%  "
            f"PWR {int(self.power*100)} FOD {int(self.food*100)} WTR {int(self.water*100)}  "
            f"CAPS {self.caps}",
            (20, 36),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (220, 220, 220),
            2,
            cv2.LINE_AA,
        )
        # Resource bars
        for i, (val, col) in enumerate(
            [
                (self.power, (0, 220, 255)),
                (self.food, (0, 200, 0)),
                (self.water, (255, 180, 0)),
            ]
        ):
            x0 = int(w * 0.35) + i * 140
            cv2.rectangle(frame, (x0, 48), (x0 + 110, 62), (40, 40, 40), -1)
            cv2.rectangle(frame, (x0, 48), (x0 + int(110 * val), 62), col, -1)

        # Dwellers — larger vault-suit sprites (blue body + yellow band)
        for d in self.dwellers:
            cx, cy = int(d.x), int(d.y)
            # legs
            cv2.rectangle(frame, (cx - 10, cy + 6), (cx - 2, cy + 28), (160, 80, 35), -1)
            cv2.rectangle(frame, (cx + 2, cy + 6), (cx + 10, cy + 28), (160, 80, 35), -1)
            # torso (blue jumpsuit)
            cv2.rectangle(frame, (cx - 12, cy - 22), (cx + 12, cy + 10), (200, 100, 45), -1)
            # yellow chest band (high sat — matches real vault suits)
            cv2.rectangle(frame, (cx - 12, cy - 8), (cx + 12, cy + 4), (35, 210, 240), -1)
            # head / hair
            cv2.circle(frame, (cx, cy - 28), 10, (170, 185, 215), -1)
            cv2.circle(frame, (cx, cy - 32), 6, (30, 30, 40), -1)

        return frame

    def status(self) -> dict[str, Any]:
        return {
            "frame": self.frame_i,
            "t": round(self.t, 2),
            "population": len(self.dwellers),
            "happiness": round(self.happiness, 3),
            "power": round(self.power, 3),
            "food": round(self.food, 3),
            "water": round(self.water, 3),
            "caps": self.caps,
            "won": self.won(),
            "ground_truth": self.ground_truth(),
        }
