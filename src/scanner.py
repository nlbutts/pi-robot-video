import os
import threading
import time
import logging

logger = logging.getLogger(__name__)

VALID_EXTENSIONS = {".mkv", ".mp4"}
MAX_BUTTON = 24


class USBScanner:
    def __init__(self, media_base="/media", poll_interval=2):
        self._media_base = media_base
        self._poll_interval = poll_interval
        self._video_map = {}
        self._lock = threading.Lock()
        self._running = False
        self._thread = None

    @property
    def video_count(self):
        with self._lock:
            return len(self._video_map)

    def get_path(self, button_num):
        with self._lock:
            return self._video_map.get(button_num)

    def get_video_map(self):
        with self._lock:
            return dict(self._video_map)

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._thread.start()
        logger.info("Scanner started (media=%s interval=%ss)", self._media_base, self._poll_interval)

    def stop(self):
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=self._poll_interval + 1)

    def _poll_loop(self):
        while self._running:
            self._scan()
            time.sleep(self._poll_interval)

    def _scan(self):
        new_map = {}
        if not os.path.isdir(self._media_base):
            return

        for root, _dirs, files in os.walk(self._media_base):
            for fname in files:
                name, ext = os.path.splitext(fname)
                ext = ext.lower()
                if ext not in VALID_EXTENSIONS:
                    continue
                try:
                    num = int(name)
                except ValueError:
                    continue
                if 1 <= num <= MAX_BUTTON:
                    full = os.path.join(root, fname)
                    if num not in new_map:
                        new_map[num] = full

        prev_count = self.video_count
        with self._lock:
            self._video_map = new_map

        if len(new_map) != prev_count:
            logger.info("Scan found %d video(s)", len(new_map))
