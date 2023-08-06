from pycad import COM
from pycad import SPI


class OnStart:
    @staticmethod
    def init_all():
        com = COM.TitanCOM()
        com.start_com()
        spi = SPI.VMXSPI()
        spi.start_spi()


if __name__ == "__main__":
    OnStart.init_all()
