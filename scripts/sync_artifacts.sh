#!/usr/bin/env bash
# Synchronize code and experiment artifacts between local machine and a remote worker.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET_HOST="${1:-pc}"
DIRECTION="${2:-push}" # push (local -> remote) or pull (remote -> local)

case "${DIRECTION}" in
  push)
    echo "==> Pushing workspace to ${TARGET_HOST}:~/Developer/phaistos-disk/"
    ssh "${TARGET_HOST}" "mkdir -p ~/Developer/phaistos-disk"
    rsync -av \
      --exclude '.venv' \
      --exclude '__pycache__' \
      --exclude '.pytest_cache' \
      --exclude '.ruff_cache' \
      --exclude '.git' \
      "${REPO_ROOT}/" \
      "${TARGET_HOST}":~/Developer/phaistos-disk/
    ;;
  pull)
    echo "==> Pulling experiment runs and reports from ${TARGET_HOST}:~/Developer/phaistos-disk/"
    mkdir -p "${REPO_ROOT}/experiments/runs"
    rsync -av \
      "${TARGET_HOST}":~/Developer/phaistos-disk/experiments/runs/ \
      "${REPO_ROOT}/experiments/runs/" || true
    rsync -av \
      "${TARGET_HOST}":~/Developer/phaistos-disk/experiments/registry.yaml \
      "${REPO_ROOT}/experiments/registry.yaml" || true
    ;;
  *)
    echo "Unknown direction: ${DIRECTION}. Use 'push' or 'pull'."
    exit 1
    ;;
esac
