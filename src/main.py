import logging
import signal
from queue import Queue, Empty

from config import BUTTON_PINS, MEDIA_PATH, SPLASH_PATH, DEBOUNCE_MS, SCAN_INTERVAL, VLC_OPTIONS
from scanner import USBScanner
from buttons import ButtonHandler
from player import VideoPlayer

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    logger.info("Starting pi-robot-video")

    scanner = USBScanner(media_base=MEDIA_PATH, poll_interval=SCAN_INTERVAL)
    scanner.start()

    player = VideoPlayer(splash_path=SPLASH_PATH, scanner=scanner, vlc_options=VLC_OPTIONS)
    player.show_splash()

    button_queue = Queue()
    buttons = ButtonHandler(pins=BUTTON_PINS, queue=button_queue, debounce_ms=DEBOUNCE_MS)
    buttons.start()

    running = True

    def shutdown(_sig, _frame):
        nonlocal running
        logger.info("Shutting down")
        running = False

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        while running:
            try:
                button_num = button_queue.get(timeout=0.5)
                logger.info("Button %d pressed", button_num)
                player.press_button(button_num)
            except Empty:
                pass

            player.process_end()

    finally:
        player.stop()
        buttons.stop()
        scanner.stop()
        logger.info("Stopped")


if __name__ == "__main__":
    main()
