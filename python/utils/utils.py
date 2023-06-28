import logging


def log_handler(logs_name):
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s-%(pathname)s:%(lineno)s-%(levelname)s-%(message)s",
                        handlers=[logging.StreamHandler()])

    logger = logging.getLogger(logs_name)
    return logger


def flush_handlers(logger):
    for handler in logger.handlers:
        handler.flush()
