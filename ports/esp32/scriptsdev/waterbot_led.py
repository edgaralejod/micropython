import _thread
from machine import Pin  # type: ignore
import time


class LEDColors:
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    YELLOW = "yellow"
    CYAN = "cyan"
    MAGENTA = "magenta"
    WHITE = "white"
    OFF = "off"


class WaterBotLED:
    def __init__(
        self,
        red_led: Pin,
        green_led: Pin,
        blue_led: Pin,
    ) -> None:
        self._red_led = red_led
        self._green_led = green_led
        self._blue_led = blue_led
        self._blink_flag = False

    def _blink_thread(self, color: str) -> None:
        while self._blink_flag:
            self.led_color(color)
            time.sleep(0.5)
            self.led_color("off")
            time.sleep(0.5)

    def start_blink(self, color: str) -> None:
        if not self._blink_flag:
            self._blink_flag = True
            _thread.start_new_thread(self._blink_thread, (color,))

    def stop_blink(self) -> None:
        self._blink_flag = False
        self.turn_off_led()

    def turn_off_led(self) -> None:
        self._red_led.off()
        self._green_led.off()
        self._blue_led.off()

    def led_color(self, color: LEDColors) -> None:
        if color == LEDColors.RED:
            self._red_led.on()
            self._green_led.off()
            self._blue_led.off()
        elif color == LEDColors.GREEN:
            self._red_led.off()
            self._green_led.on()
            self._blue_led.off()
        elif color == LEDColors.BLUE:
            self._red_led.off()
            self._green_led.off()
            self._blue_led.on()
        elif color == LEDColors.YELLOW:
            self._red_led.on()
            self._green_led.on()
            self._blue_led.off()
        elif color == LEDColors.CYAN:
            self._red_led.off()
            self._green_led.on()
            self._blue_led.on()
        elif color == LEDColors.MAGENTA:
            self._red_led.on()
            self._green_led.off()
            self._blue_led.on()
        elif color == LEDColors.WHITE:
            self._red_led.on()
            self._green_led.on()
            self._blue_led.on()
        elif color == LEDColors.OFF:
            self._red_led.off()
            self._green_led.off()
            self._blue_led.off()
        else:
            raise ValueError("Invalid color")
