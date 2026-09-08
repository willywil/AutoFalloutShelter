#!/usr/bin/env bash
# Idempotent setup for the AutoFalloutShelter development environment.
# Installs system libraries required by OpenCV and PyAutoGUI, then builds a
# Python virtual environment with the project and development dependencies.
set -euo pipefail

cd "$(dirname "$0")/.."

# System libraries:
#   libgl1 / libglib2.0-0  -> OpenCV (cv2) runtime
#   python3.12-venv        -> `python -m venv`
#   python3-tk             -> PyAutoGUI dialogs
#   scrot / xdotool        -> PyAutoGUI screenshots and window control
#   xvfb                   -> virtual display so the GUI stack imports headless
export DEBIAN_FRONTEND=noninteractive
sudo apt-get update -qq
sudo apt-get install -y --no-install-recommends \
  libgl1 \
  libglib2.0-0 \
  python3-venv \
  python3.12-venv \
  python3-dev \
  python3-tk \
  scrot \
  xdotool \
  xvfb

if [ ! -x venv/bin/python ]; then
  python3 -m venv venv
fi

./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt
# Extra developer tooling documented in docs/CONTRIBUTING.md.
./venv/bin/pip install pytest-cov mypy pre-commit

echo "AutoFalloutShelter environment setup complete."
