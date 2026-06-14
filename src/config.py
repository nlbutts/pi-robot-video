import os

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BUTTON_PINS = [
    5, 6, 12, 13, 16, 17, 22, 23, 24, 25, 26, 27,
    4, 7, 8, 9, 10, 11, 18, 19, 20, 21, 14, 15,
]

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
