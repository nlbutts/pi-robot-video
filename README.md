# pi-robot-video

A Raspberry Pi video player that responds to 17 physical button inputs.
Each button maps to a video file on a USB stick.

## Hardware

- Raspberry Pi 3 (or newer) connected to an HDMI monitor
- 17 momentary buttons wired from GPIO pins to GND
- USB memory stick for video storage

### GPIO Wiring

| Button | BCM Pin |
|--------|---------|
| 1 | 4 |
| 2 | 27 |
| 3 | 21 |
| 4 | 13 |
| 5 | 26 |
| 6 | 23 |
| 7 | 22 |
| 8 | 12 |
| 9 | 20 |
| 10 | 19 |
| 11 | 24 |
| 12 | 25 |
| 13 | 5 | 
| 14 | 6 | 
| 15 | 16 | 
| 16 | 17 | 
| 17 | 18 |

Each button connects its GPIO pin to a GND pin (e.g., 6, 9, 14, 20, 25, 30, 34, 39).
The internal pull-up resistor keeps the pin HIGH; pressing the button pulls it LOW.

## Video Files

Place video files on a USB stick with the naming convention `01.mkv` through `17.mkv`
(or `.mp4`). The file number corresponds to the button number.

```
USB_ROOT/
  01.mkv
  02.mp4
  03.mkv
  ...
  17.mp4
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

## Testing video playback

Test a video on the display from the command line:

```bash
WAYLAND_DISPLAY=wayland-0 XDG_RUNTIME_DIR=/run/user/1000 cvlc --fullscreen --no-osd --play-and-exit /media/usb/01.mp4
```

## Installation

On the Raspberry Pi, clone this repo into the home directory:

```bash
git clone <repo-url> ~/pi-robot-video
cd ~/pi-robot-video
chmod +x scripts/install.sh
./scripts/install.sh
```

The install script:
1. Installs system packages (`vlc`, `python3-pip`, `python3-gpiozero`, `exfatprogs`)
2. Installs `python-vlc` via pip
3. Installs a udev rule to auto-mount USB drives to `/media/usb`
4. Enables auto-login via `raspi-config`
5. Creates the `/run/user` runtime directory if needed

After installation, reboot and the video player starts automatically via the desktop autologin.

## Deployment

Deploy the code to the Raspberry Pi using `rsync` or `scp`:

```bash
# Using rsync (recommended):
rsync -avz ~/pi-robot-video/ robots@pi:~/pi-robot-video/

# Using scp:
scp -r ~/pi-robot-video robots@pi:~/
```

Target: `robots@pi` (password: `robots`). The directory is copied to `~/pi-robot-video` on the Pi.

Run the player manually:

```bash
cd ~/pi-robot-video
python3 src/main.py
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
- **SCAN_INTERVAL** — seconds between USB media scans

## Requirements

- Raspberry Pi OS Bookworm (Desktop)
- Python 3.9+
- VLC media player
- python-vlc
- gpiozero (pre-installed on Pi OS)
