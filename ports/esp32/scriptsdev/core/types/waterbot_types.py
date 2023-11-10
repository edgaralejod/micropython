import json


class WaterBotI2CAddresses:
    """WaterBot I2C Addresses"""

    AD5934 = 0x0D
    ADG715_PORT1 = 0x48
    ADG715_PORT2 = 0x49


class LEDColors:
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    YELLOW = "yellow"
    CYAN = "cyan"
    MAGENTA = "magenta"
    WHITE = "white"


class SwitchSetting:
    """Switch Setting Enum"""

    CONDPORT = 0x40
    THERMISTOR = 0x80
    RCAL_10K = 0x20
    RCAL_1K = 0x10
    RCAL_100 = 0x08


class PortSetting:
    """Port Setting Enum"""

    PORT1 = 0x49
    PORT2 = 0x48


class PGASetting:
    """Programmable Gain Amplifier Setting Enum"""

    GAIN1 = 0x01
    GAIN5 = 0x00


class VoltageSetting:
    """Output Stimulation Voltage Setting Enum"""

    ONEV_PKPK = 0x06
    TWOV_PKPK = 0x00
    FOURHUNDREDMV_PKPK = 0x04
    TWOHUNDREDMV_PKPK = 0x02


class AnalogFrontEndGain:
    """Analog Front End Gain Setting Enum"""

    GAIN_R_FBK_100 = 0x01
    GAIN_R_FBK_1K = 0x02
    GAIN_R_FBK_10K = 0x04


class DataPoint:
    """Data Point Class"""

    def __init__(
        self, current_freq: int, img_val: int, real_val: int, magnitude: float
    ) -> None:
        self.current_freq = current_freq
        self.img_val = img_val
        self.real_val = real_val
        self.magnitude = magnitude

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "DataPoint":
        """Converts Dictionary to Data Point"""
        return cls(
            current_freq=int(data["current_freq"]),
            img_val=int(data["img_val"]),
            real_val=int(data["real_val"]),
            magnitude=float(data["magnitude"]),
        )

    @classmethod
    def from_json(cls, json_str: str) -> "DataPoint":
        """Converts JSON String to Data Point"""
        data = json.loads(json_str)
        return cls(
            current_freq=data["current_freq"],
            img_val=data["img_val"],
            real_val=data["real_val"],
            magnitude=data["magnitude"],
        )

    def to_dict(self) -> dict:
        """Converts Data Point to Dictionary"""
        return {
            "current_freq": self.current_freq,
            "img_val": self.img_val,
            "real_val": self.real_val,
            "magnitude": self.magnitude,
        }


class DeviceSettings:
    """Device Settings Class"""

    def __init__(
        self,
        pkpkvolt: VoltageSetting = VoltageSetting.TWOV_PKPK,
        intpga: PGASetting = PGASetting.GAIN1,
        portsetting: PortSetting = PortSetting.PORT1,
        switchsetting: SwitchSetting = SwitchSetting.CONDPORT,
        numbersamples: int = 2,
        sample_req: int = 2,
        sample_remain: int = 0,
        afegain: AnalogFrontEndGain = AnalogFrontEndGain.GAIN_R_FBK_1K,
        startfreq: int = 3000,
        freqinc: int = 100,
    ) -> None:
        self.pkpkvolt = pkpkvolt
        self.intpga = intpga
        self.portsetting = portsetting
        self.switchsetting = switchsetting
        self.numbersamples = numbersamples
        self.sample_req = sample_req
        self.sample_remain = sample_remain
        self.afegain = afegain
        self.startfreq = startfreq
        self.freqinc = freqinc

    @property
    def pkpkvolt(self) -> VoltageSetting:
        """Returns pkpkvolt"""
        return self._pkpkvolt

    @pkpkvolt.setter
    def pkpkvolt(self, value: VoltageSetting) -> None:
        """Sets pkpkvolt"""
        self._pkpkvolt = value

    @property
    def intpga(self) -> PGASetting:
        """Returns intpga"""
        return self._intpga

    @intpga.setter
    def intpga(self, value: PGASetting) -> None:
        """Sets intpga"""
        self._intpga = value

    @property
    def portsetting(self) -> PortSetting:
        """Returns portsetting"""
        return self._portsetting

    @portsetting.setter
    def portsetting(self, value: PortSetting) -> None:
        """Sets portsetting"""
        self._portsetting = value

    @property
    def switchsetting(self) -> SwitchSetting:
        """Returns switchsetting"""
        return self._switchsetting

    @switchsetting.setter
    def switchsetting(self, value: SwitchSetting) -> None:
        """Sets switchsetting"""
        self._switchsetting = value

    @property
    def numbersamples(self) -> int:
        """Returns numbersamples"""
        return self._numbersamples

    @numbersamples.setter
    def numbersamples(self, value: int) -> None:
        """Sets numbersamples"""
        self._numbersamples = value

    @property
    def sample_req(self) -> int:
        """Returns sample_req"""
        return self._sample_req

    @sample_req.setter
    def sample_req(self, value: int) -> None:
        """Sets sample_req"""
        self._sample_req = value

    @property
    def sample_remain(self) -> int:
        """Returns sample_remain"""
        return self._sample_remain

    @sample_remain.setter
    def sample_remain(self, value: int) -> None:
        """Sets sample_remain"""
        self._sample_remain = value

    @property
    def afegain(self) -> AnalogFrontEndGain:
        """Returns afegain"""
        return self._afegain

    @afegain.setter
    def afegain(self, value: AnalogFrontEndGain) -> None:
        """Sets afegain"""
        self._afegain = value

    @property
    def startfreq(self) -> int:
        """Returns startfreq"""
        return self._startfreq

    @startfreq.setter
    def startfreq(self, value: int) -> None:
        """Sets startfreq"""
        self._startfreq = value

    @property
    def freqinc(self) -> int:
        """Returns freqinc"""
        return self._freqinc

    @freqinc.setter
    def freqinc(self, value: int) -> None:
        """Sets freqinc"""
        self._freqinc = value

    def to_dict(self) -> dict:
        """Converts Device Settings to Dictionary"""
        return {
            "pkpkvolt": self.pkpkvolt.value,
            "intpga": self.intpga.value,
            "portsetting": self.portsetting.value,
            "switchsetting": self.switchsetting.value,
            "numbersamples": self.numbersamples,
            "sample_req": self.sample_req,
            "sample_remain": self.sample_remain,
            "afegain": self.afegain.value,
            "startfreq": self.startfreq,
            "freqinc": self.freqinc,
        }
