from contextlib import contextmanager
from logging import getLogger, FileHandler,  Formatter,  StreamHandler
from logging import INFO
import time


# @contextmanager
# def timer(name):
#     t0 = time.time()
#     LOGGER.info(f'[{name}] start')
#     yield
#     LOGGER.info(f'[{name}] done in {time.time() - t0:.0f} s.')


def init_logger(log_file):
    logger = getLogger(__name__)
    logger.setLevel(INFO)
    handler1 = StreamHandler()
    handler1.setFormatter(Formatter("%(message)s"))
    handler2 = FileHandler(filename=log_file)
    handler2.setFormatter(Formatter("%(message)s"))
    logger.addHandler(handler1)
    logger.addHandler(handler2)
    
    return logger