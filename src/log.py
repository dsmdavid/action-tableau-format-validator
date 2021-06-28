import logging
import sys
from logging import Logger
from logging.handlers import TimedRotatingFileHandler
import os

logger_levels = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG' : logging.DEBUG
}
class MyLogger(Logger):
    def __init__(
        self,
        log_file=None,
        log_format="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s",
        log_path='',
        *args,
        **kwargs
    ):
        self.formatter = logging.Formatter(log_format)
        if log_path:
            if not os.path.exists(log_path):
                os.makedirs(log_path)

        self.log_file = os.path.join(log_path, log_file)


        Logger.__init__(self, *args, **kwargs)

        self.addHandler(self.get_console_handler())
        if log_file:
            self.addHandler(self.get_file_handler())

        # with this pattern, it's rarely necessary to propagate the| error up to parent
        self.propagate = False

    def get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        return console_handler

    def get_file_handler(self):
        file_handler = TimedRotatingFileHandler(self.log_file, when="midnight")
        file_handler.setFormatter(self.formatter)
        return file_handler