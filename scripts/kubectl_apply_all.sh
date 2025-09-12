#!/usr/bin/env bash
set -euo pipefail
echo "[*] Applying Kubernetes manifests..."
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/mongo-pvc.yaml
kubectl apply -f k8s/mongo-deployment.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/service-lb.yaml
echo "[✓] Applied. Get external IP with:"
echo "kubectl -n honey-shop get svc honey-backend"
