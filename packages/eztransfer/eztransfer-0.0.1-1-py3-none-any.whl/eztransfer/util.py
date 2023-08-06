import inspect
import logging
import shutil
import sys

LOGGER_NAME = "eztransfer"


def get_logger(module_name: str = None):
    logger = logging.getLogger(LOGGER_NAME)
    return logger.getChild(module_name) if module_name else logger


def setup_logger(logger_name: str = LOGGER_NAME, filename: str = None, level=logging.DEBUG):
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)

    logger.handlers.clear()
    logger.addHandler(sh)

    if filename:
        fh = logging.FileHandler(filename)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


def typename(cls) -> str:
    return type(cls).__name__


def remove_dir(path: str, ignore_errors: bool = False):
    logger = get_logger(__name__)
    try:
        shutil.rmtree(path)
    except Exception as e:
        logger.warning(f"Cannot remove temporary directory {path!r}: {e!r}")
        if not ignore_errors:
            raise


def auto_repr(cls):
    members = vars(cls)

    if "__repr__" in list(members):
        raise TypeError(f"{typename(cls)} already defines __repr__")

    parameter_names = list(inspect.signature(cls).parameters)

    if not all(isinstance(members.get(name), property) for name in parameter_names):
        raise TypeError(
            f"Cannot apply auto_repr to {typename(cls)} because not all __init__ parameters have matching properties.")

    def new_repr(self):
        args = [(name, getattr(self, name)) for name in parameter_names]
        str_args = ", ".join(f"{name}={value!r}" for name, value in args)
        return f"{typename(self)}({str_args})"

    setattr(cls, "__repr__", new_repr)

    return cls


def insert_logger(cls):
    cls.logger = get_logger(cls.__name__)
    return cls
