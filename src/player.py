import os
import threading
import logging

import vlc

logger = logging.getLogger(__name__)


class VideoPlayer:
    def __init__(self, splash_path, scanner, vlc_options=None):
        self._splash_path = splash_path
        self._scanner = scanner
        self._vlc_options = vlc_options or []

        self._queue_video = None
        self._is_playing = False
        self._current_button = None
        self._ending = False
        self._end_reached = threading.Event()

        self._instance = vlc.Instance(*self._vlc_options)
        self._player = self._instance.media_player_new()
        self._player.set_fullscreen(True)

        events = self._player.event_manager()
        events.event_attach(vlc.EventType.MediaPlayerEndReached, self._on_video_end)
        events.event_attach(vlc.EventType.MediaPlayerEncounteredError, self._on_video_error)

    def show_splash(self):
        if not os.path.isfile(self._splash_path):
            logger.warning("Splash image not found: %s", self._splash_path)
            return
        self._ending = True
        self._player.stop()
        self._end_reached.clear()
        media = self._instance.media_new(self._splash_path)
        media.add_option("image-duration=-1")
        self._player.set_media(media)
        self._player.play()
        self._is_playing = False
        self._current_button = None
        self._ending = False
        logger.info("Splash displayed")

    def press_button(self, button_num):
        if self._is_playing:
            self._queue_video = button_num
            logger.debug("Queued video %d (replaces previous queue)", button_num)
        else:
            self._play_video(button_num)

    def process_end(self):
        if not self._end_reached.is_set():
            return

        self._end_reached.clear()
        self._is_playing = False
        self._current_button = None

        if self._queue_video is not None:
            next_button = self._queue_video
            self._queue_video = None
            self._play_video(next_button)
        else:
            self.show_splash()

    def stop(self):
        self._player.stop()
        try:
            self._player.release()
        except Exception:
            pass
        try:
            self._instance.release()
        except Exception:
            pass

    def _play_video(self, button_num):
        path = self._scanner.get_path(button_num)
        if not path:
            logger.info("No video file for button %d", button_num)
            return

        if not os.path.isfile(path):
            logger.warning("Video file missing: %s", path)
            return

        self._ending = True
        self._player.stop()
        self._end_reached.clear()
        media = self._instance.media_new(path)
        self._player.set_media(media)
        self._player.play()
        self._is_playing = True
        self._current_button = button_num
        self._queue_video = None
        self._ending = False
        logger.info("Playing video %d: %s", button_num, os.path.basename(path))

    def _on_video_end(self, event):
        if not self._ending:
            self._end_reached.set()

    def _on_video_error(self, event):
        if not self._ending:
            logger.warning("VLC error — returning to splash")
            self._end_reached.set()
