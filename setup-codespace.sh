#!/usr/bin/env bash
set -e

echo "=== 1. Verificando e instalando Minikube si no existe ==="
if ! command -v minikube &> /dev/null; then
  curl -sLO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
  sudo install minikube-linux-amd64 /usr/local/bin/minikube
  rm -f minikube-linux-amd64
fi

echo "=== 2. Verificando e instalando kubectl si no existe ==="
if ! command -v kubectl &> /dev/null; then
  curl -sLO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
  sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
  rm -f kubectl
fi

echo "=== 3. Instalando dependencias de Python para las pruebas ==="
pip install -q -r backend/requirements.txt pytest

echo "=== LISTO: Minikube ($(minikube version --short)) y Kubectl instalados ==="
