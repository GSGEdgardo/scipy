#  Copyright (c) 2025.  Departamento de Ingenieria de Sistemas y Computacion
import logging

import coloredlogs
from typeguard import typechecked


@typechecked
def configure_logging() -> None:
    log_level = logging.DEBUG
    log_format = \
        "%(asctime)s [%(levelname)8s] %(name)s:%(lineno)d (%(process)d/%(threadName)s)  - %(message)s"

    coloredlogs.install(
        level=log_level,
        fmt=log_format,
        level_styles={
            "debug": {"color": "cyan"},
            "info": {"color": "green"},
            "warning": {"color": "yellow"},
            "error": {"color": "red"},
            "critical": {"color": "red", "bold": True},
        },
        field_styles={
            "asctime": {"color": "cyan"},
            "levelname": {"bold": True},
            "name": {"color": "blue", "bold": True},
            "lineno": {"color": "magenta"},
            "process": {"color": "green"},
            "threadName": {"color": "yellow"},
            "message": {"color": "black"},
        },
        milliseconds=True,
    )