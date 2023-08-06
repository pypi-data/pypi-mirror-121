import logging


FORMAT = '[%(levelname)s] (%(threadName)-10s) %(message)s'

logging.basicConfig(level=logging.DEBUG,
                    format=FORMAT)

file_handler = logging.FileHandler('/home/pi/main.log')
file_handler.setFormatter(logging.Formatter(FORMAT))
main_logger = logging.getLogger("main_logger")
main_logger.addHandler(file_handler)

file_handler = logging.FileHandler('/home/pi/spi.log')
file_handler.setFormatter(logging.Formatter(FORMAT))
spi_logger = logging.getLogger("spi_logger")
spi_logger.addHandler(file_handler)

file_handler = logging.FileHandler('/home/pi/com.log')
file_handler.setFormatter(logging.Formatter(FORMAT))
com_logger = logging.getLogger("com_logger")
com_logger.addHandler(file_handler)


def write_spi_log(s: str):
    spi_logger.info(s)


def write_com_log(s: str):
    com_logger.info(s)


def write_main_log(s: str):
    main_logger.info(s)
