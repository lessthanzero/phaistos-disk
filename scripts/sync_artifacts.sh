#!/usr/bin/env bash
# Synchronize code and experiment artifacts between local machine and Fedora PC worker
set -euo pipefail

TARGET_HOST="${1:-pc}"
DIRECTION="${2:-push}" # push (Mac -> PC) or pull (PC -> Mac)

case "${DIRECTION}" in
  push)
    echo "==> Pushing workspace to ${TARGET_HOST}:~/Developer/phaistos-disk/"
    rsync -av \
      --exclude '.venv' \
      --exclude '__pycache__' \
      --exclude '.pytest_cache' \
      --exclude '.ruff_cache' \
      /Users/sashakatin/Developer/phaistos-disk/ \
      "${TARGET_HOST}":~/Developer/phaistos-disk/
    ;;
  pull)
    echo "==> Pulling experiment runs and reports from ${TARGET_HOST}:~/Developer/phaistos-disk/"
    rsync -av \
      "${TARGET_HOST}":~/Developer/phaistos-disk/experiments/runs/ \
      /Users/sashakatin/Developer/phaistos-disk/experiments/runs/
    rsync -av \
      "${TARGET_HOST}":~/Developer/phaistos-disk/experiments/registry.yaml \
      /Users/sashakatin/Developer/phaistos-disk/experiments/registry.yaml
    ;;
  *)
    echo "Unknown direction: ${DIRECTION}. Use 'push' or 'pull'."
    exit 1
    ;;
esac
