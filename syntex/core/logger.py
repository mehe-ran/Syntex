import logging
import sys

def setup_logger(name: str = "syntex") -> logging.Logger:
    # initialize the logger
    logger = logging.getLogger(name)
    
    # set default log level
    logger.setLevel(logging.DEBUG)

    # check if handlers already exist to prevent duplicate logs
    if not logger.handlers:
        # create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)

        # define log format
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)

        # add handler to logger
        logger.addHandler(console_handler)

    return logger

logger = setup_logger()
