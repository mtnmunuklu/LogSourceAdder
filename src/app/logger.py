import logging
import os
from src.config import Config


class Logger:

    """
    Used for logging
    """

    def __init__(self, log_type):
        """
        Constructor function
        :param log_type: type of log(database or webcrawler vs.)
        """
        self.log_type = log_type
        self.log_dir = Config.LOG_DIR
        self.log_path = self.log_dir + Config.LOG_FILE
        self.log_format = Config.LOG_FORMAT
        self.close_log()
        self.logger = self.get_log_config()

    def log(self, level, msg):
        """
        Log info/warning/error message in log file.
        """
        if self.logger is not None:
            if level == logging.INFO:
                self.logger.info("{}".format(msg))
            elif level == logging.WARNING:
                self.logger.warning("{}".format(msg))
            else:
                self.logger.error("{}".format(msg))

    def get_log_config(self):
        """
        Configuration for logging
        :return:
        """
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # create logger
        logger = logging.getLogger(self.log_type)
        # create handler
        file_path = os.path.abspath(self.log_path)
        handler = logging.FileHandler(file_path)
        # create formatter
        formatter = logging.Formatter(self.log_format)
        # set Formatter
        handler.setFormatter(formatter)
        # add handler
        logger.addHandler(handler)
        # set level
        logger.setLevel(logging.INFO)

        return logger
    

    def close_log(self):
        """
        Remove all logger
        :return: None
        """
        logger = logging.getLogger(self.log_type)
        while logger.hasHandlers():
            logger.removeHandler(logger.handlers[0])
