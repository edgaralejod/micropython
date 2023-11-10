class AD5934AddressDefinitions:
    """AD5934 address definitions from datasheet"""

    AD5934_REG_CONTROL_HB = 0x80  # R/W, 2 bytes
    AD5934_REG_CONTROL_LB = 0x81  # R/W, 2 bytes
    AD5934_REG_FREQ_START_HB = 0x82  # R/W, 3 bytes
    AD5934_REG_FREQ_START_MB = 0x83
    AD5934_REG_FREQ_START_LB = 0x84
    AD5934_REG_FREQ_INC_HB = 0x85  # R/W, 3 bytes
    AD5934_REG_FREQ_INC_MB = 0x86
    AD5934_REG_FREQ_INC_LB = 0x87
    AD5934_REG_INC_NUM_HB = 0x88  # R/W, 2 bytes, 9 bit
    AD5934_REG_INC_NUM_LB = 0x89
    AD5934_REG_SETTLING_CYCLES_HB = 0x8A  # R/W, 2 bytes
    AD5934_REG_SETTLING_CYCLES_LB = 0x8B
    AD5934_REG_STATUS = 0x8F  # R, 1 byte
    AD5934_REG_TEMP_DATA_HB = 0x92  # R, 2 bytes
    AD5934_REG_TEMP_DATA_LB = 0x93
    AD5934_REG_REAL_DATA_HB = 0x94  # R, 2 bytes
    AD5934_REG_REAL_DATA_LB = 0x95
    AD5934_REG_IMAG_DATA_HB = 0x96  # R, 2 bytes
    AD5934_REG_IMAG_DATA_LB = 0x97


class AD5934ControlRegisterDefinitions:
    """AD5934 control register definitions from datasheet"""

    AD5934_CLOCK_EXTERNAL = 0x08
    AD5934_CLOCK_INTERNAL = 0x00
    AD5934_RESET = 0x10


class AD5934StatusRegisterDefinitions:
    """AD5934 status register definitions from datasheet"""

    AD5934_VALID_DATA = 0x02
    AD5934_FREQ_SWEEP_CMPL = 0x04


class AD5934I2CCommandDefinitions:
    """AD5934 command definitions from datasheet"""

    AD5934_SET_POINTER_COMMAND = 0xB0
    AD5934_BLOCK_WRITE = 0xA0
    AD5934_BLOCK_READ = 0xA1


class AD5934ControlModeDefinitions:
    """AD5934 control mode definitions from datasheet"""

    AD5934_INIT_START_FREQ = 0x10
    AD5934_START_FREQ_SWP = 0x20
    AD5934_INC_FREQ = 0x30
    AD5934_REPEAT_FREQ = 0x40
    AD5934_PWD_DOWN = 0xA0
    AD5934_STANDBY = 0xB0

class AD5934SweepStates:
    """AD5934 sweep states"""

    INIT = 0
    START = 1
    INC = 2
    REPEAT = 3
    FINISH = 4
    DONE = 5