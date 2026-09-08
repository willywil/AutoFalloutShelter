"""Dweller detectors tuned against real Fallout Shelter vault frames.

Verified empirically on assets/screenshots/*.png — do not trust thresholds
without re-running tests/test_dweller_detect.py after changes.
"""

from __future__ import annotations

from typing import Iterable

import cv2
import numpy as np

from src.models.dweller import Detection


def playable_mask(h: int, w: int) -> np.ndarray:
    """Binary mask: 1 = playable vault band, 0 = HUD/chrome/dirt margins."""
    m = np.ones((h, w), np.uint8)
    m[: int(h * 0.14), :] = 0  # top HUD
    m[int(h * 0.82) :, :] = 0  # bottom chrome
    m[:, : int(w * 0.02)] = 0
    m[:, int(w * 0.94) :] = 0
    m[int(h * 0.72) :, : int(w * 0.18)] = 0
    m[int(h * 0.72) :, int(w * 0.80) :] = 0
    return m


def _suppress_collect_icons(hsv: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Remove floating lime collect icons (lightning / fork) that fake dwellers."""
    lime = cv2.inRange(hsv, np.array([35, 140, 140]), np.array([95, 255, 255]))
    lime = cv2.dilate(lime, np.ones((15, 15), np.uint8), iterations=1)
    return cv2.bitwise_and(mask, cv2.bitwise_not(lime))


def detect_vault_suit_blobs(frame: np.ndarray) -> list[Detection]:
    """Detect vault-suit dwellers via blue jumpsuit + yellow stripe colors.

    This is the primary detector — vault suits are the most stable appearance
    cue across zoom levels. Green collect icons are explicitly suppressed.
    """
    h, w = frame.shape[:2]
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    ui = playable_mask(h, w)

    # Vault suit: yellow chest band + blue fabric
    yellow = cv2.inRange(hsv, (15, 70, 70), (42, 255, 255))
    blue = cv2.inRange(hsv, (85, 35, 35), (135, 255, 230))
    # Skin / hair mid tones (helps when yellow stripe is occluded)
    skin = cv2.inRange(hsv, (5, 40, 60), (25, 160, 230))

    suit = cv2.bitwise_or(yellow, blue)
    suit = cv2.bitwise_or(suit, cv2.bitwise_and(skin, blue))  # skin near blue
    # Prefer regions that contain BOTH yellow and blue nearby (true vault suits)
    yellow_d = cv2.dilate(yellow, np.ones((11, 11), np.uint8), iterations=1)
    blue_d = cv2.dilate(blue, np.ones((11, 11), np.uint8), iterations=1)
    both = cv2.bitwise_and(yellow_d, blue_d)
    suit = cv2.bitwise_or(suit, both)

    suit = cv2.bitwise_and(suit, ui * 255)
    suit = _suppress_collect_icons(hsv, suit)

    # Kill sand / sky / near-black rock false positives
    sand = cv2.inRange(hsv, (8, 20, 100), (35, 90, 220))
    sky = cv2.inRange(hsv, (80, 5, 140), (120, 70, 255))
    rock = cv2.inRange(hsv, (0, 0, 0), (180, 80, 40))
    bg = cv2.bitwise_or(cv2.bitwise_or(sand, sky), rock)
    suit = cv2.bitwise_and(suit, cv2.bitwise_not(bg))

    suit = cv2.morphologyEx(suit, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    suit = cv2.morphologyEx(suit, cv2.MORPH_CLOSE, np.ones((9, 7), np.uint8))

    contours, _ = cv2.findContours(suit, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    out: list[Detection] = []
    for c in contours:
        area = float(cv2.contourArea(c))
        if area < 70 or area > 9000:
            continue
        x, y, bw, bh = cv2.boundingRect(c)
        if bh < 18 or bw < 8:
            continue
        # People are taller than wide (allow mild merges)
        if bw > bh * 1.9:
            continue
        cx = x + bw / 2.0
        cy = y + bh * 0.55
        # Keep door-queue exterior candidates (left wasteland)
        if cy < h * 0.16 or cy > h * 0.78:
            continue
        # Score: prefer yellow+blue overlap and upright aspect
        roi_y = yellow[y : y + bh, x : x + bw]
        roi_b = blue[y : y + bh, x : x + bw]
        y_frac = float(roi_y.mean()) / 255.0 if roi_y.size else 0.0
        b_frac = float(roi_b.mean()) / 255.0 if roi_b.size else 0.0
        aspect = bh / max(bw, 1)
        score = min(1.0, area / 1500.0) * (0.35 + 0.35 * y_frac + 0.30 * b_frac)
        score *= min(1.4, aspect / 1.6)
        if score < 0.08:
            continue
        out.append(Detection(cx, cy, float(bw), float(bh), float(score), "suit"))
    return _nms(out, iou_thresh=0.35)


def detect_color_blobs(frame: np.ndarray) -> list[Detection]:
    """Broader clothing-color detector (secondary; used when suits fail)."""
    h, w = frame.shape[:2]
    ui = playable_mask(h, w)
    # Floor band where dwellers stand
    ui[: int(h * 0.22), :] = 0
    ui[int(h * 0.76) :, :] = 0

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    sat, val = hsv[:, :, 1], hsv[:, :, 2]
    mask = ((sat > 45) & (val > 35) & (val < 240)).astype(np.uint8) * 255
    sand = cv2.inRange(hsv, (8, 20, 100), (35, 90, 220))
    sky = cv2.inRange(hsv, (80, 5, 140), (120, 70, 255))
    rock = cv2.inRange(hsv, (0, 0, 0), (180, 80, 45))
    mask = cv2.bitwise_and(mask, cv2.bitwise_not(sand))
    mask = cv2.bitwise_and(mask, cv2.bitwise_not(sky))
    mask = cv2.bitwise_and(mask, cv2.bitwise_not(rock))
    mask = cv2.bitwise_and(mask, ui * 255)
    mask = _suppress_collect_icons(hsv, mask)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 7), np.uint8))

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    out: list[Detection] = []
    for c in contours:
        area = float(cv2.contourArea(c))
        if area < 90 or area > 6000:
            continue
        x, y, bw, bh = cv2.boundingRect(c)
        if bh < 16 or bw < 6 or bw > bh * 2.0:
            continue
        cx, cy = x + bw / 2.0, y + bh * 0.55
        if cy < h * 0.24 or cy > h * 0.74:
            continue
        score = min(1.0, area / 1200.0) * (bh / max(bw, 1)) / 3.0
        out.append(Detection(cx, cy, float(bw), float(bh), float(score), "color"))
    return _nms(out, iou_thresh=0.4)


def detect_motion_blobs(
    prev_gray: np.ndarray | None,
    gray: np.ndarray,
) -> list[Detection]:
    """Moving person-sized regions via frame difference."""
    if prev_gray is None or prev_gray.shape != gray.shape:
        return []
    h, w = gray.shape[:2]
    ui = playable_mask(h, w)
    ui[: int(h * 0.22), :] = 0
    ui[int(h * 0.76) :, :] = 0
    diff = cv2.absdiff(prev_gray, gray)
    _, th = cv2.threshold(diff, 18, 255, cv2.THRESH_BINARY)
    th = cv2.bitwise_and(th, ui * 255)
    th = cv2.morphologyEx(th, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, np.ones((7, 9), np.uint8))
    contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    out: list[Detection] = []
    for c in contours:
        area = float(cv2.contourArea(c))
        if area < 60 or area > 8000:
            continue
        x, y, bw, bh = cv2.boundingRect(c)
        if bh < 12:
            continue
        cx, cy = x + bw / 2.0, y + bh / 2.0
        if cy < h * 0.24 or cy > h * 0.74:
            continue
        out.append(
            Detection(cx, cy, float(bw), float(max(bh, 20)), min(1.0, area / 800.0), "motion")
        )
    return out


def merge_detections(
    primary: Iterable[Detection],
    secondary: Iterable[Detection],
    dist: float = 30.0,
) -> list[Detection]:
    """Keep primary detections; add secondary only when spatially novel."""
    merged = list(primary)
    for d in secondary:
        if all((d.cx - m.cx) ** 2 + (d.cy - m.cy) ** 2 > dist**2 for m in merged):
            merged.append(d)
        else:
            for i, m in enumerate(merged):
                if (d.cx - m.cx) ** 2 + (d.cy - m.cy) ** 2 <= dist**2:
                    if d.score > m.score:
                        merged[i] = Detection(
                            m.cx, m.cy, m.w, m.h, max(m.score, d.score) + 0.1, m.source
                        )
                    break
    return merged


def detect_dwellers(
    frame: np.ndarray,
    prev_gray: np.ndarray | None = None,
) -> list[Detection]:
    """Full per-frame detection: vault suits + color + motion."""
    suits = detect_vault_suit_blobs(frame)
    colors = detect_color_blobs(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    motion = detect_motion_blobs(prev_gray, gray)
    # Prefer suits; fold in non-overlapping color/motion
    merged = merge_detections(suits, colors, dist=28.0)
    merged = merge_detections(merged, motion, dist=28.0)
    return sorted(merged, key=lambda d: -d.score)


def annotate_detections(frame: np.ndarray, dets: list[Detection]) -> np.ndarray:
    out = frame.copy()
    for d in dets:
        x0 = int(d.cx - d.w / 2)
        y0 = int(d.cy - d.h / 2)
        x1 = int(d.cx + d.w / 2)
        y1 = int(d.cy + d.h / 2)
        color = (0, 220, 0) if d.source == "suit" else (0, 180, 255)
        if d.source == "motion":
            color = (255, 128, 0)
        cv2.rectangle(out, (x0, y0), (x1, y1), color, 2)
        cv2.circle(out, d.as_int, 3, (0, 0, 255), -1)
        cv2.putText(
            out,
            f"{d.source[0]}{d.score:.2f}",
            (x0, max(16, y0 - 4)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            color,
            1,
            cv2.LINE_AA,
        )
    return out


def _iou(a: Detection, b: Detection) -> float:
    ax0, ay0 = a.cx - a.w / 2, a.cy - a.h / 2
    ax1, ay1 = a.cx + a.w / 2, a.cy + a.h / 2
    bx0, by0 = b.cx - b.w / 2, b.cy - b.h / 2
    bx1, by1 = b.cx + b.w / 2, b.cy + b.h / 2
    ix0, iy0 = max(ax0, bx0), max(ay0, by0)
    ix1, iy1 = min(ax1, bx1), min(ay1, by1)
    inter = max(0.0, ix1 - ix0) * max(0.0, iy1 - iy0)
    union = a.w * a.h + b.w * b.h - inter
    return inter / union if union else 0.0


def _nms(dets: list[Detection], iou_thresh: float = 0.4) -> list[Detection]:
    kept: list[Detection] = []
    for d in sorted(dets, key=lambda x: -x.score):
        if all(_iou(d, k) < iou_thresh for k in kept):
            kept.append(d)
    return kept
