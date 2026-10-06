#!/usr/bin/env bash
set -euo pipefail

IMAGE_TAG="${TAG:-latest}"
NAMESPACE="fanous"

echo "Building backend image..."
docker build -t "fanous-backend:${IMAGE_TAG}" ./backend

echo "Building frontend image..."
docker build -t "fanous-frontend:${IMAGE_TAG}" ./frontend

echo "Loading images into K3s..."
k3s ctr images import --no-compress <(docker save "fanous-backend:${IMAGE_TAG}")
k3s ctr images import --no-compress <(docker save "fanous-frontend:${IMAGE_TAG}")

echo "Applying K3s manifests..."
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml
kubectl apply -f k8s/ingress.yaml

echo "Waiting for pods to be ready..."
kubectl rollout status deployment/backend -n "${NAMESPACE}" --timeout=300s
kubectl rollout status deployment/frontend -n "${NAMESPACE}" --timeout=120s

echo ""
echo "Deployed! Access at: http://fanous.local"
