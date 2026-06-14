# pi-robot-video

A Raspberry Pi video player that responds to 24 physical button inputs.
Each button maps to a video file on a USB stick.

## Hardware

- Raspberry Pi 3 (or newer) connected to an HDMI monitor
- 24 momentary buttons wired from GPIO pins to GND
- USB memory stick for video storage

### GPIO Wiring

| Button | BCM Pin | Physical Pin |
|--------|---------|-------------|
| 1 | 5 | 29 |
| 2 | 6 | 31 |
| 3 | 12 | 32 |
| 4 | 13 | 33 |
| 5 | 16 | 36 |
| 6 | 17 | 11 |
| 7 | 22 | 15 |
| 8 | 23 | 16 |
| 9 | 24 | 18 |
| 10 | 25 | 22 |
| 11 | 26 | 37 |
| 12 | 27 | 13 |
| 13 | 4 | 7 |
| 14 | 7 | 26 |
| 15 | 8 | 24 |
| 16 | 9 | 21 |
| 17 | 10 | 19 |
| 18 | 11 | 23 |
| 19 | 18 | 12 |
| 20 | 19 | 35 |
| 21 | 20 | 38 |
| 22 | 21 | 40 |
| 23 | 14 | 8 |
| 24 | 15 | 10 |

Each button connects its GPIO pin to a GND pin (e.g., 6, 9, 14, 20, 25, 30, 34, 39).
The internal pull-up resistor keeps the pin HIGH; pressing the button pulls it LOW.

## Video Files

Place video files on a USB stick with the naming convention `01.mkv` through `24.mkv`
(or `.mp4`). The file number corresponds to the button number.

```
USB_ROOT/
  01.mkv
  02.mp4
  03.mkv
  ...
  24.mp4
```

For best performance on the Pi 3, encode videos as **H.264** in an `.mp4` or `.mkv`
container. Higher-bitrate or non-H.264 codecs may struggle with software decoding.

## Behavior

- When idle, a splash screen image is displayed (fullscreen).
- Press a button: the corresponding video plays immediately.
- While a video is playing, pressing another button queues that video.
  The **most recent** button press wins (only one video is queued at a time).
- When the current video finishes, the queued video plays automatically.
- If a button has no matching video file on the USB stick, the press is ignored.
- Plug in or remove the USB stick at any time; videos are rescanned every 2 seconds.

## Installation

On the Raspberry Pi, clone this repo into the home directory:

```bash
git clone <repo-url> ~/pi-robot-video
cd ~/pi-robot-video
chmod +x scripts/install.sh
./scripts/install.sh
```

The install script:
1. Installs system packages (`vlc`, `python3-pip`, `python3-gpiozero`)
2. Installs `python-vlc` via pip
3. Installs and enables a systemd user service
4. Enables linger so the service starts at boot

After installation, enable auto-login via `sudo raspi-config`:
- System Options → Boot / Auto Login → Desktop Autologin

Reboot, and the video player starts automatically.

### Manual control

```bash
systemctl --user start pi-video.service
systemctl --user stop pi-video.service
systemctl --user status pi-video.service
journalctl --user -u pi-video.service -f
```

## Testing without GPIO

To test on a PC without GPIO hardware, press Enter in the terminal.
Each Enter press simulates button 1 being pressed.

## Configuration

Edit `src/config.py` to change:
- **BUTTON_PINS** — GPIO BCM pin assignments
- **MEDIA_PATH** — base path to scan for USB media (default `/media`)
- **SPLASH_PATH** — path to the splash screen image
- **DEBOUNCE_MS** — button debounce time in milliseconds
- **VLC_OPTIONS** — additional VLC command-line options

## Requirements

- Raspberry Pi OS Bookworm (Desktop or Lite)
- Python 3.9+
- VLC media player
- gpiozero (pre-installed on Pi OS)
- python-vlc
