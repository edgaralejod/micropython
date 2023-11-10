from machine import Pin, I2C  # type: ignore
from core.controllers.waterbot_led import WaterBotLED
from core.controllers.generic_state_machine import GenericStateMachine
from core.types.waterbot_types import (
    WaterBotI2CAddresses,
    LEDColors,
    PGASetting,
    VoltageSetting,
    DataPoint,
)
from core.types.ad5934_types import (
    AD5934AddressDefinitions,
    AD5934ControlRegisterDefinitions,
    AD5934ControlModeDefinitions,
    AD5934SweepStates,
)
from core.drivers.adg715 import ADG715
from core.drivers.ad5934 import AD5934


class WaterbotEmbeddedController:
    """Waterbot Embedded Controller Class"""

    def __init__(self, i2c: I2C, red_led: Pin, green_led: Pin, blue_led: Pin):
        self._read_values = []
        self._sweep_data = []
        self._read_sweep: DataPoint = DataPoint()
        self._read_magnitude = -1
        self._current_frequency = 0
        self._increment_frequency_setting = 0
        self._stored_frequency_setting = 0
        self._voltage_setting: VoltageSetting = VoltageSetting.TWOV_PKPK
        self._pga_setting: PGASetting = PGASetting.GAIN1
        self._led = WaterBotLED(red_led, green_led, blue_led)
        self._port1_switch = ADG715(i2c, WaterBotI2CAddresses.ADG715_PORT1)
        self._port2_switch = ADG715(i2c, WaterBotI2CAddresses.ADG715_PORT2)
        self._ad5934 = AD5934(i2c, i2c_addr=WaterBotI2CAddresses.AD5934)
        self._state: AD5934SweepStates = AD5934SweepStates.INIT
        self._state_machine = GenericStateMachine()

    def init_state_machine(self):
        self._state_machine.add_state_handler(AD5934SweepStates.INIT, self.sweep_init)

    def set_increment_number(self, num_increments):
        """Set the number of increments for the frequency sweep"""
        increment = self.long_to_bytearray(num_increments)
        self._ad5934.write_register(
            AD5934AddressDefinitions.AD5934_REG_INC_NUM_HB, increment[1]
        )
        self._ad5934.write_register(
            AD5934AddressDefinitions.AD5934_REG_INC_NUM_LB, increment[0]
        )

    def set_frequency(self, frequency, register_hb, register_mb, register_lb):
        """Set the frequency for the frequency sweep"""
        freq_calc = round((2**27) * (frequency) / (self._ad5934.clock / 16))
        new_freq_calc = self.long_to_bytearray(freq_calc)
        self._ad5934.write_register(register_hb, new_freq_calc[2])
        self._ad5934.write_register(register_mb, new_freq_calc[1])
        self._ad5934.write_register(register_lb, new_freq_calc[0])

    def set_start_frequency(self, frequency):
        """Set the start frequency for the frequency sweep"""
        self.set_frequency(
            frequency,
            AD5934AddressDefinitions.AD5934_REG_FREQ_START_HB,
            AD5934AddressDefinitions.AD5934_REG_FREQ_START_MB,
            AD5934AddressDefinitions.AD5934_REG_FREQ_START_LB,
        )

    def set_increment_frequency(self, frequency):
        """Set the increment frequency for the frequency sweep"""
        self.set_frequency(
            frequency,
            AD5934AddressDefinitions.AD5934_REG_FREQ_INC_HB,
            AD5934AddressDefinitions.AD5934_REG_FREQ_INC_MB,
            AD5934AddressDefinitions.AD5934_REG_FREQ_INC_LB,
        )

    # Function that converts rounded int of the frequency calculation to an array of 8 bytes
    def long_to_bytearray(self, long_number):
        bytearray = [None] * 8
        for i in range(0, len(bytearray)):
            byte = int(long_number) & 0xFF
            bytearray[i] = byte
            long_number = (long_number - byte) / 256
        return bytearray

    def clear_values_and_get_status(self) -> list:
        """Clear and get values from the I2C bus"""
        self._read_values = []  # Clear past read values
        return self._ad5934.get_values(AD5934AddressDefinitions.AD5934_REG_STATUS, 1)

    def sweep_init(self):
        self._current_frequency = self._stored_frequency_setting

        self._ad5934.write_register(
            AD5934AddressDefinitions.AD5934_REG_CONTROL_LB,
            AD5934ControlRegisterDefinitions.AD5934_CLOCK_EXTERNAL
            | AD5934ControlRegisterDefinitions.AD5934_RESET,
        )

        self._ad5934.write_register(
            AD5934AddressDefinitions.AD5934_REG_CONTROL_HB,
            AD5934ControlModeDefinitions.AD5934_STANDBY
            | self._voltage_setting
            | self._pga_setting,
        )

        self._ad5934.write_register(
            AD5934AddressDefinitions.AD5934_REG_CONTROL_HB,
            AD5934ControlModeDefinitions.AD5934_INIT_START_FREQ
            | self._voltage_setting
            | self._pga_setting,
        )

        self._ad5934.write_register(
            AD5934AddressDefinitions.AD5934_REG_CONTROL_HB,
            AD5934ControlModeDefinitions.AD5934_START_FREQ_SWP
            | self._voltage_setting
            | self._pga_setting,
        )

        self.clear_values_and_get_status()
        return self._sweep_process()

    # This method computes the impedance and it populates and creates the
    # data structures that then get sent to the cloud.
    def sweepIncrement(self):
        self._led.led_color_toggle(LEDColors.YELLOW)
        self._AD5934GetValues(self._AD5934_REG_REAL_DATA_HB, 4)

        # print(self._read_values)
        # print("RawReal")
        # print(self._read_values[1])
        # print(self._read_values[2])
        # print("RawImg")
        # print(self._read_values[3])
        # print(self._read_values[4])
        realVal = self._read_values[1] + self._read_values[2]
        imgVal = self._read_values[3] + self._read_values[4]

        # print("Sums")
        # print(realVal)
        # print(imgVal)
        realVal = (int(self._read_values[1], 16) << 8) + int(self._read_values[2], 16)
        imgVal = (int(self._read_values[3], 16) << 8) + int(self._read_values[4], 16)
        if (realVal & 0x8000) > 1:
            realVal = realVal - 0x10000
        if (imgVal & 0x8000) > 1:
            imgVal = imgVal - 0x10000

        # print("Real and imaginary to signed")
        # print(realVal)
        # print(imgVal)
        self._read_sweep["current_frequency"] = self._current_frequency
        self._read_sweep["imgVal"] = imgVal
        self._read_sweep["realVal"] = realVal
        realVal = realVal**2
        imgVal = imgVal**2
        self._read_magnitude = (realVal + imgVal) ** 0.5
        self._read_sweep["magnitude"] = self._read_magnitude
        self._sweep_data.append(dict(self._read_sweep))
        self._current_frequency = (
            self._current_frequency + self._increment_frequency_setting
        )
        cfgReg = self._voltage_setting | self._pga_setting | self._AD5934_INC_FREQ
        self._AD5934WriteRegister(self._AD5934_REG_CONTROL_HB, cfgReg)
        self._clearAndGetValue()
        self._sweepProcess()
        # sleep(0.2)
        self._led.led_off()

    def sweep_process(self):
        hexcompare = self._read_values[0]
        # original = self._read_values[0]
        # print("No transformation:")
        # print(hexcompare)
        # print("Transformed")
        hexcompare = hexcompare[1]
        # print(hexcompare)
        if hexcompare == "0":
            while hexcompare == "0":
                # print("I am in a loop")
                hexcompare = self._read_values[0]
                # print("No transformation:")
                # print(hexcompare)
                # print("Transformed")
                hexcompare = hexcompare[1]
                # print(hexcompare)
                self._clearAndGetValue()

        if hexcompare == "2":
            self._sweepIncrement()

        elif hexcompare == "6":
            pass
            # print("done")
        else:
            raise OSError("Analog Subsystem Failure")

    def init_analog_system(self):
        self.set_frequency(1000)
        self.set_increment_frequency(500)
        self.set_increment_number(1)
        self._AD5934WriteRegister(
            self._AD5934_REG_CONTROL_LB,
            self._AD5934_CLOCK_EXTERNAL | self._AD5934_RESET,
        )
        # sleep(0.2)
        self._AD5934WriteRegister(
            self._AD5934_REG_CONTROL_LB, self._AD5934_CLOCK_EXTERNAL
        )
        # sleep(0.2)
        self._AD5934WriteRegister(
            self._AD5934_REG_CONTROL_HB,
            self._AD5934_STANDBY | self._AD5934_2V_PP | self._AD5934_PGA_1,
        )
        # sleep(0.2)
        self._ADG715_clear_channel(self._ADG715_1)
        self._ADG715_clear_channel(self._ADG715_2)
        # print("AD5934 Init method")

    def setAnalogSwitch(self, swNum, afeGain, portSetting):
        self._ADG715_clear_channel(self._ADG715_1)
        self._ADG715_clear_channel(self._ADG715_2)
        self._ADG715_set_channel(swNum, afeGain | portSetting)
        # print("Setting Analog Switch")

    def sweepCommand(self, gain, startFreq, incFreq, voltage, incNum):
        self._led.led_off()
        self._led.led_color_set(LEDColors.YELLOW)
        print("On sweep Command")
        self._AD5934SetStartFrequency(startFreq)
        self._AD5934SetIncrementFrequency(incFreq)
        self._AD5934SetIncrementNumber(incNum)
        self._voltage_setting = voltage
        self._pga_setting = gain
        self._stored_frequency_setting = startFreq
        self._increment_frequency_setting = incFreq
        self._sweepInit()
        self._led.led_color_set(LEDColors.GREEN)
        # print(self._sweep_data)
        return self._sweep_data

    def clearSweepObject(self):
        self._sweep_data = []
        return
