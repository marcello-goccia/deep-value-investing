#!/usr/bin/env python
# -*- coding: iso8859-15 -*-
#-*-coding:utf-8-*-

"""
@package loggingHWI
File for logging the code
It can display a different message according to the type.
It could be info, warning, error or exception.
"""

import logging.config

import os
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.realpath(os.path.join(dir_path, '..'))

root_folder_all_code = f"{os.path.basename(parent_path)}/"

logs_directory = "logs"
name_log_file = "status.log"
dir_root = dir_path.split(root_folder_all_code, 1)[0]
log_path = os.path.join(dir_root, root_folder_all_code, logs_directory)
log_file_path = os.path.join(log_path, name_log_file)

if not os.path.exists(log_path):
    os.mkdir(log_path)


def initLogger():
    """
    @function initLogger
    It initialises the file logger.
    """
    dictLogConfig = {
        "version": 1,
        "handlers": {
                    "rotHandler": {
                        "class": "logging.handlers.RotatingFileHandler",
                        "formatter": "myFormatter",
                        "filename": log_file_path,
                        "maxBytes":  500000,
                        "backupCount": 10,
                        }
                    },
        "loggers": {
            "wristbotDash": {
                "handlers": ["rotHandler"],
                "level": "INFO",
                }
            },

        "formatters": {
            "myFormatter": {
                "format": "%(asctime)s-%(levelname)s- %(message)s"
                }
            }
        }

    logging.config.dictConfig(dictLogConfig)
    return logging.getLogger("wristbotDash")

def info(message):
    """
    @function info
    Different message in case of an info message.
    """
    logger = initLogger()
    logger.info(message)
    print(message)

def warning(message):
    """
    @function warning
    Different message in case of a warning message.
    """
    logger = initLogger()
    logger.warning(message)
    print(message)

def error(message):
    """
    @function error
    Different message in case of an error message.
    """
    logger = initLogger()
    logger.error(message)
    print(message)

def exception(message):
    """
    @function exception
    Different message in case of an exception message.
    """
    logger = initLogger()
    logger.exception(message)
    print(message)
