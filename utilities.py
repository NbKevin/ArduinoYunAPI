#!/usr/env/bin python

"""
Useful utilities for flask.
"""

from flask import Flask

from config_ import YUN_API_CONFIG

__author__ = 'Nb'


def set_up_flask(flask: Flask):
    """
    Set up flask configurations.

    @param flask: Flask instance.
    """
    config = {
        'DEBUG': YUN_API_CONFIG.flask_debug
    }
    flask.config.update(**config)
