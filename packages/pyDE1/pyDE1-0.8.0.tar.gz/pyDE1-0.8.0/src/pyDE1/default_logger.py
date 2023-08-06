"""
Copyright © 2021 Jeff Kletsky. All Rights Reserved.

License for this software, part of the pyDE1 package, is granted under
GNU General Public License v3.0 only
SPDX-License-Identifier: GPL-3.0-only
"""

import logging
from logging.handlers import QueueHandler
import os
import multiprocessing

from typing import Optional


def set_some_logging_levels():
    asyncio_logger = logging.getLogger('asyncio')
    asyncio_logger.setLevel(logging.INFO)
    bleak_logger = logging.getLogger('bleak')
    bleak_logger.setLevel(logging.INFO)
    logging.getLogger(multiprocessing.current_process().name).info(
        f"Levels: {asyncio_logger}, {bleak_logger}"
    )


def initialize_default_logger(
        log_queue: Optional[multiprocessing.Queue] = None):

    format_string = "%(asctime)s %(levelname)s [%(processName)s] " \
                    "%(name)s: %(message)s"

    # logfile_directory = '_logs'

    logging.basicConfig(level=logging.DEBUG,
                        format=format_string,
                        )

    # It looks like steerr handler comes with "basicConfig"
    #     root.handlers = [<StreamHandler <stderr> (NOTSET)>]

    logger = logging.getLogger(multiprocessing.current_process().name)

    if log_queue is not None:
        lq = QueueHandler(log_queue)
        # Formatting is done by the handler for QueueListener
        # lq.setFormatter(logging.Formatter(format_string))
        lq.setLevel(logging.DEBUG)
        logging.getLogger().addHandler(lq)
        logger.info(f"Enabled logging handler {lq}")
