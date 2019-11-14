import datetime as dt
import logging
import logging.handlers

import config


def bootstrap():
    init_logging()


def init_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(config.LOG_LEVEL)

    log_formatter = logging.Formatter(
        fmt='%(asctime)s.%(msecs)03d:' + logging.BASIC_FORMAT,
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    file_handler = logging.handlers.RotatingFileHandler(
        config.LOG_FILE_NAME,
        maxBytes=config.LOGFILE_MAXSIZE_BYTES,
        encoding='utf-8',
    )
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)
    root_logger.info(f'\n\n\n======================== New log: {dt.datetime.now()} ========================')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)
