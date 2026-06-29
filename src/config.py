import os

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BUTTON_PINS = [4, 27, 21, 13, 26, 23, 22, 12, 20, 19, 24, 25, 5, 6, 16, 17, 18]

MEDIA_PATH = "/media"

SPLASH_PATH = os.path.join(_PROJECT_ROOT, "fm_stem_alliance.png")

DEBOUNCE_MS = 200

SCAN_INTERVAL = 2

VLC_OPTIONS = [
    "--image-duration=-1",
    "--fullscreen",
    "--no-osd",
    "--no-video-title-show",
    "--verbose=-1",
    "--intf=dummy",
    "--no-qt-privacy-ask",
    "--no-disable-screensaver",
]
