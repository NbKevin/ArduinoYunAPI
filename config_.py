#!/usr/env/bin python
# -*- encoding: utf-8 -*-

"""
Yun API config.
"""

import os

from yun.config import Config

__author__ = 'Nb'

DEFAULT_YUN_API_CONFIG_PATH = os.path.join(
    os.path.dirname(__file__),
    'config', 'yun_api.cfg'
)


class YunAPIConfig(Config):
    """Flask config."""

    def __init__(self, path: str):
        super().__init__(path)

    @property
    def flask_host(self):
        return self._config['flask']['host']

    @property
    def flask_port(self):
        return int(self._config['flask']['port'])

    @property
    def flask_address(self):
        return ':'.join([self.flask_host, str(self.flask_port)])

    @property
    def flask_debug(self):
        return self._config['flask']['debug']


YUN_API_CONFIG = YunAPIConfig(DEFAULT_YUN_API_CONFIG_PATH)
