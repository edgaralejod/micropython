from machine import I2C  # type: ignore


class ADG715:
    """ADG715 class"""

    def __init__(self, i2c: I2C, addr=0x48) -> None:
        self.i2c = i2c
        self.addr = addr

    def set(self, channel) -> None:
        """Sets the channel"""
        self.i2c.writeto(self.addr, bytes([channel]))

    def clear(self) -> None:
        """Clears the channel"""
        self.i2c.writeto(self.addr, bytes([0]))

    def get(self) -> int:
        """Gets the channel"""
        return self.i2c.readfrom(self.addr, 1)[0]
