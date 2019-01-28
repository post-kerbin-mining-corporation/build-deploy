import logging


def set_logging(log_name):
    """
    Configures logging

    Inputs:
        log_name (string): The base log name for this logging session
    """
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    logger.addHandler(ch)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    return logger
