from multiprocessing import Process
import spidev

from pycad import Logger


class VMXSPI:
    def __init__(self):
        try:
            self.spi = spidev.SpiDev()
            self.spi.open(1, 2)
        except (Exception, EOFError) as e:
            Logger.spi_logger.info(e.__repr__())

    def start_spi(self) -> None:
        proc = Process(target=self.spi_loop, name='pycad_spi')
        proc.start()

    def spi_loop(self) -> None:
        pass

