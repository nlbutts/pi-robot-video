import logging
import threading
from queue import Queue

logger = logging.getLogger(__name__)

try:
    from gpiozero import Button
    from gpiozero.exc import GPIODeviceError

    _GPIO_AVAILABLE = True
except ImportError:
    _GPIO_AVAILABLE = False
    Button = None
    GPIODeviceError = Exception


class ButtonHandler:
    def __init__(self, pins, queue, debounce_ms=200):
        self._pins = pins
        self._queue = queue
        self._debounce = debounce_ms / 1000.0
        self._buttons = []
        self._mock = not _GPIO_AVAILABLE

    def start(self):
        if self._mock:
            logger.warning("GPIO unavailable — buttons are MOCKED (press Enter for button 1)")
            self._sim_thread = threading.Thread(target=self._simulate, daemon=True)
            self._sim_thread.start()
            return

        for idx, pin in enumerate(self._pins, 1):
            try:
                btn = Button(pin, pull_up=False, bounce_time=self._debounce)
                btn.when_pressed = self._make_callback(idx)
                btn.when_released = self._make_release_callback(idx)
                self._buttons.append(btn)
            except GPIODeviceError as exc:
                logger.error("Failed to init GPIO %d: %s", pin, exc)
        logger.info("Button handler started: %d buttons on GPIO (3.3V wiring, pull_up=False)", len(self._buttons))

    def stop(self):
        if self._mock:
            return
        for btn in self._buttons:
            btn.close()
        self._buttons.clear()

    def _make_callback(self, button_num):
        def cb():
            logger.info("Button %d PRESSED (GPIO edge detected)", button_num)
            self._queue.put(button_num)
        return cb

    def _make_release_callback(self, button_num):
        def cb():
            logger.debug("Button %d released", button_num)
        return cb

    def _simulate(self):
        while True:
            try:
                input()
                self._queue.put(1)
                logger.debug("Mock button 1 pressed")
            except EOFError:
                break
