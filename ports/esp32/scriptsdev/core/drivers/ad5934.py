from machine import I2C  # type: ignore
from core.types.ad5934_types import AD5934I2CCommandDefinitions


class AD5934:
    """AD5934 class"""

    def __init__(self, i2c: I2C, clock: float = 16e6, i2c_addr=0x0D) -> None:
        self._i2c = i2c
        self._i2c_addr = i2c_addr
        self._i2c = i2c
        self._clock = clock

    @property
    def clock(self) -> float:
        """Returns clock"""
        return self._clock

    @clock.setter
    def clock(self, value: float) -> None:
        """Sets clock"""
        self._clock = value

    def write_register(self, addr, data) -> None:
        """Writes to a register"""
        data_arr = []
        data_arr.append(data)
        data_bytes = bytes(data_arr)
        self._i2c.writeto_mem(self._i2c_addr, addr, data_bytes)

    def set_pointer(self, addr) -> None:
        """Sets the pointer to a register"""
        add_arr = []
        add_arr.append(AD5934I2CCommandDefinitions.AD5934_SET_POINTER_COMMAND)
        add_bytes = bytes(add_arr)
        self._i2c.writeto_mem(self._i2c_addr, addr, add_bytes)

    def get_values(self, init_addr, num) -> list:
        """Gets the values from the registers"""
        self.set_pointer(init_addr)
        return_arr = []
        # print("I am getting the values")
        for i in range(0, num):
            read_value = self._i2c.readfrom(self._i2c_addr, 1)
            hex_val = ord(read_value)
            return_arr.append("{0:02x}".format(hex_val))
        return return_arr

    def read_pointer(self) -> None:
        """Reads the pointer, debugging only"""
        print(self._i2c.readfrom(self._i2c_addr, 1))
