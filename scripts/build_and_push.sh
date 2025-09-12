#!/usr/bin/env bash
set -euo pipefail
IMAGE="mohammadsadeg/honey-backend"
TAG="v1"
echo "[*] Building image: $IMAGE:$TAG"
docker build -f docker/Dockerfile.prod -t "$IMAGE:$TAG" -t "$IMAGE:latest" .
echo "[*] Pushing..."
docker push "$IMAGE:$TAG"
docker push "$IMAGE:latest"
echo "[✓] Done. Pushed $IMAGE:{latest,$TAG}"
