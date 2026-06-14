#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
SERVICE_SRC="$PROJECT_DIR/systemd/pi-video.service"
UDEV_SRC="$PROJECT_DIR/udev/99-usb-mount.rules"
SERVICE_DEST="/etc/systemd/system/pi-video.service"
UDEV_DEST="/etc/udev/rules.d/99-usb-mount.rules"

echo "=== Pi Robot Video Player Installer ==="
echo "Project: $PROJECT_DIR"
echo ""

# --- System dependencies ---
echo "[1/7] Installing system packages..."
sudo apt-get update -qq
sudo apt-get install -y vlc python3-pip python3-gpiozero exfatprogs

# --- Python dependencies ---
echo "[2/7] Installing Python packages..."
pip3 install --break-system-packages python-vlc

# --- Systemd system service ---
echo "[3/7] Installing systemd service..."
sed "s|__PROJECT_DIR__|$PROJECT_DIR|g" "$SERVICE_SRC" | sudo tee "$SERVICE_DEST" > /dev/null
sudo systemctl daemon-reload
sudo systemctl enable pi-video.service

# --- Udev rule for USB auto-mount ---
echo "[4/7] Installing udev rule..."
sudo cp "$UDEV_SRC" "$UDEV_DEST"
sudo udevadm control --reload-rules

# --- Enable auto-login for desktop session ---
echo "[5/7] Enabling auto-login for user '$USER'..."
if command -v raspi-config &>/dev/null; then
    sudo raspi-config nonint do_boot_behaviour B4
    echo "Auto-login enabled via raspi-config."
else
    echo "WARNING: raspi-config not found. Auto-login NOT configured."
    echo "Run 'sudo raspi-config' -> System Options -> Boot -> Desktop Autologin"
fi

# --- Verify Wayland socket path ---
echo "[6/7] Setting up runtime directory..."
SOCKET_DIR="/run/user/$(id -u)"
if [ ! -d "$SOCKET_DIR" ]; then
    sudo mkdir -p "$SOCKET_DIR"
    sudo chown "$USER":"$USER" "$SOCKET_DIR"
    echo "Created $SOCKET_DIR"
fi

# --- Mount any already-plugged-in USB and start service ---
echo "[7/7] Starting service..."
sudo mkdir -p /media/usb
sudo systemctl start pi-video.service
sleep 2
sudo systemctl status pi-video.service --no-pager

echo ""
echo "Installation complete."
echo ""
echo "To view logs:  journalctl -u pi-video.service -f"
echo "To stop:       sudo systemctl stop pi-video.service"
echo "To restart:    sudo systemctl restart pi-video.service"
