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
        self._toggle_flag = False

    def _blink_thread(self, color: str) -> None:
        while self._blink_flag:
            self.led_color_set(color)
            time.sleep(0.5)
            self.led_off()
            time.sleep(0.5)

    def start_blink(self, color: str) -> None:
        if not self._blink_flag:
            self._blink_flag = True
            _thread.start_new_thread(self._blink_thread, (color,))

    def stop_blink(self) -> None:
        self._blink_flag = False
        self.led_color

    def led_off(self) -> None:
        self._toggle_flag = False
        self._red_led.off()
        self._green_led.off()
        self._blue_led.off()

    def led_color_toggle(self, color:LEDColors) -> None:
        if self._toggle_flag:
            self.led_off()
        else:
            self.led_color_set(color)

    def led_color_set(self, color: LEDColors) -> None:
        self._toggle_flag = True
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

        else:
            raise ValueError("Invalid color")
