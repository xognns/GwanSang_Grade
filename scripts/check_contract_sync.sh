#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! cmp -s docs/api/analysis-api.openapi.yaml specs/001-face-grade-mvp/contracts/analysis-api.openapi.yaml; then
  echo "[ERROR] API contract drift detected: docs/api/analysis-api.openapi.yaml != specs/001-face-grade-mvp/contracts/analysis-api.openapi.yaml"
  echo "Re-run docs generation or copy canonical contract into Docs/API."
  exit 1
fi

if ! cmp -s docs/schemas/result-card-view-model.schema.json specs/001-face-grade-mvp/contracts/result-card-view-model.schema.json; then
  echo "[ERROR] Result schema drift detected: docs/schemas/result-card-view-model.schema.json != specs/001-face-grade-mvp/contracts/result-card-view-model.schema.json"
  echo "Re-run docs generation or copy canonical schema into Docs/Schemas."
  exit 1
fi

echo "[OK] Contract sync check passed."
