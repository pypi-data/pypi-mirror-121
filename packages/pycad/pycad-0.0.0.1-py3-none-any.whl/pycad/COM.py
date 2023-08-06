from multiprocessing import Process
from typing import Optional

import serial

from pycad import Logger


class TitanCOM:
    def __init__(self):
        try:
            self.ser = serial.Serial(
                port='/dev/ttyACM0',
                baudrate=115200,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
            )
            self.ser.open()
        except (Exception, serial.SerialException) as e:
            Logger.com_logger.info(e.__repr__())

    def start_com(self) -> None:
        proc = Process(target=self.com_loop, name='pycad_com')
        proc.start()

    def com_loop(self) -> None:
        pass

    def send_data(self, data: bytearray) -> None:
        self.ser.write(data)

    def read_data(self) -> Optional[bytes]:
        return self.ser.read()
