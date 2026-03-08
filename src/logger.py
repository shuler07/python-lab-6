import logging


class Logger:
    def __init__(self):
        logging.basicConfig(filename="shell.log", filemode="a",level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%d.%m.%Y %H:%M:%S')
        self.logger = logging.getLogger()

    def info(self, msg: str, *args) -> None:
        self.logger.info(msg, *args)

    def warning(self, msg: str, *args) -> None:
        self.logger.warning(msg, *args)

    def error(self, msg: str, *args) -> None:
        self.logger.error(msg, *args)

    def critical(self, msg: str, *args) -> None:
        self.logger.critical(msg, *args)

logger = Logger()
