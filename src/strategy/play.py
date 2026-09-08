"""Strategy that plays the vault simulator toward a win.

Uses tracked dweller IDs (when available) and ground-truth for assignment
decisions. Collects ready rooms, balances staffing, recruits population.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.models.dweller import Track
from src.sim.vault_sim import VaultSim


@dataclass
class PlayResult:
    steps: int
    won: bool
    final_status: dict[str, Any]
    log: list[dict[str, Any]] = field(default_factory=list)


def _nearest_track(tracks: list[Track], x: float, y: float) -> Track | None:
    if not tracks:
        return None
    return min(tracks, key=lambda t: (t.cx - x) ** 2 + (t.cy - y) ** 2)


def play_to_win(
    sim: VaultSim,
    *,
    max_steps: int = 800,
    tracks_provider=None,
) -> PlayResult:
    """Run autonomous vault management until win or max_steps.

    tracks_provider: optional callable(frame) -> list[Track] for CV-driven play.
    If None, uses simulator ground truth (still validates economy strategy).
    """
    log: list[dict[str, Any]] = []
    for step in range(max_steps):
        sim.step(1 / 12)
        frame = sim.render()
        tracks: list[Track] = []
        if tracks_provider is not None:
            tracks = tracks_provider(frame)

        # Collect ready rooms
        for room in sim.rooms:
            if room.ready:
                ok = sim.collect(room.name)
                log.append({"step": step, "act": "collect", "room": room.name, "ok": ok})

        # Staff underfilled production rooms
        counts = {r.name: 0 for r in sim.rooms}
        for d in sim.dwellers:
            counts[d.room] = counts.get(d.room, 0) + 1

        need_order = []
        for kind, name in (("power", "power"), ("water", "water"), ("diner", "diner")):
            room = next(r for r in sim.rooms if r.name == name)
            if counts.get(name, 0) < 2:
                need_order.append(room)

        # Sources: living / overstaffed
        sources = [
            d
            for d in sim.dwellers
            if d.room in ("living", "storage", "door")
            or counts.get(d.room, 0) > 3
        ]
        for room in need_order:
            if not sources:
                break
            d = sources.pop(0)
            # If CV tracks exist, prefer nearest track to dweller for identity glue
            if tracks:
                tr = _nearest_track(tracks, d.x, d.y)
                if tr is not None:
                    log.append(
                        {
                            "step": step,
                            "act": "track_link",
                            "sid": d.sid,
                            "tid": tr.tid,
                            "dist": round(((tr.cx - d.x) ** 2 + (tr.cy - d.y) ** 2) ** 0.5, 1),
                        }
                    )
            ok = sim.assign(d.sid, room.name)
            counts[d.room] = max(0, counts.get(d.room, 1) - 1)
            counts[room.name] = counts.get(room.name, 0) + 1
            log.append({"step": step, "act": "assign", "sid": d.sid, "to": room.name, "ok": ok})

        # Grow population toward win
        if len(sim.dwellers) < sim.cfg.win_population and step % 25 == 0:
            ok = sim.recruit()
            log.append({"step": step, "act": "recruit", "ok": ok, "pop": len(sim.dwellers)})

        if sim.won():
            return PlayResult(step + 1, True, sim.status(), log[-80:])

    return PlayResult(max_steps, False, sim.status(), log[-80:])
