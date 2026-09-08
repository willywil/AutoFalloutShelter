#!/usr/bin/env bash
# Per-boot startup: ensure a virtual X display is available so the GUI
# automation stack (PyAutoGUI / Pillow ImageGrab) can be imported and run
# headlessly. Idempotent: does nothing if a display is already serving :99.
set -euo pipefail

if ! xdpyinfo -display :99 >/dev/null 2>&1; then
  Xvfb :99 -screen 0 1920x1080x24 >/tmp/xvfb.log 2>&1 &
  # Give Xvfb a moment to come up.
  for _ in $(seq 1 10); do
    if xdpyinfo -display :99 >/dev/null 2>&1; then
      break
    fi
    sleep 0.5
  done
fi

echo "Virtual display :99 ready."
