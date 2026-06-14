#!/usr/bin/env bash
set -euo pipefail

PI_IP="192.168.1.225"
PI_USER="robots"
PI_PASS="robots"
PI_HOME="/home/${PI_USER}"
PROJECT_NAME="pi-robot-video"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=== Deploy to Raspberry Pi ==="
echo "Target: ${PI_USER}@${PI_IP}"
echo "Source: ${PROJECT_DIR}"
echo ""

if ! command -v sshpass &>/dev/null; then
    echo "[0] Installing sshpass..."
    sudo apt-get update -qq
    sudo apt-get install -y sshpass
fi

echo "[1] Testing connection..."
if ! sshpass -p "${PI_PASS}" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 "${PI_USER}@${PI_IP}" 'echo OK' 2>/dev/null; then
    echo "ERROR: Cannot reach ${PI_USER}@${PI_IP}"
    exit 1
fi

echo "[2] Syncing files..."
sshpass -p "${PI_PASS}" rsync -avz --delete \
    --exclude='.opencode/' \
    --exclude='__pycache__/' \
    --exclude='*.pyc' \
    --exclude='.git/' \
    -e 'ssh -o StrictHostKeyChecking=no' \
    "${PROJECT_DIR}/" \
    "${PI_USER}@${PI_IP}:${PI_HOME}/${PROJECT_NAME}/"

echo "[3] Running install script..."
sshpass -p "${PI_PASS}" ssh -o StrictHostKeyChecking=no "${PI_USER}@${PI_IP}" \
    "cd ${PI_HOME}/${PROJECT_NAME} && chmod +x scripts/install.sh && ./scripts/install.sh"

echo "[4] Starting service..."
sshpass -p "${PI_PASS}" ssh -o StrictHostKeyChecking=no "${PI_USER}@${PI_IP}" \
    "sudo systemctl start pi-video.service"

echo ""
echo "Deploy complete."
echo ""
echo "Service status:"
sshpass -p "${PI_PASS}" ssh -o StrictHostKeyChecking=no "${PI_USER}@${PI_IP}" \
    "sudo systemctl status pi-video.service --no-pager" || true

echo ""
echo "Recent logs:"
sshpass -p "${PI_PASS}" ssh -o StrictHostKeyChecking=no "${PI_USER}@${PI_IP}" \
    "journalctl -u pi-video.service -n 20 --no-pager" || true
