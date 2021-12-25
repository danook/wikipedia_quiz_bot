from logging import DEBUG, FileHandler, getLogger, Formatter


def get_logger(module, filename="log/wikiqbot.log"):
    logger = getLogger(module)
    logger.setLevel(DEBUG)  # TODO: Change this to INFO
    file_handler = FileHandler(filename)
    file_handler.setLevel(DEBUG)  # TODO: Change this to INFO
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(name)s:%(lineno)s %(funcName)s [%(levelname)s]: %(message)s'))
    logger.addHandler(file_handler)
    return logger
