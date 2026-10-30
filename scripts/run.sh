#!/bin/bash
# Starts the offline app. Usage: scripts/run.sh [--port 7860]
cd "$(dirname "$0")/.." || exit 1
exec .venv/bin/python app.py "$@"
