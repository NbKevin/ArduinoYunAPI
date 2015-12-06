#!/usr/env/bin python
# -*- encoding: utf-8 -*-

"""
Config related business.
"""

import os

from yun.utilities import open_and_save, SingletonMeta

__author__ = 'Nb'

DEFAULT_YUN_CONFIG_PATH = os.path.join(
    os.path.split(os.path.split(__file__)[0])[0],
    'config', 'yun.cfg'
)


class Config:
    """The base config manager."""

    def __init__(self, path: str):
        """Initialise the manager from a config file."""
        self.config_path = path
        self._config = None
        self.load()

    def load(self):
        """Load the config."""
        with open_and_save(self.config_path, save=False) as config:
            self._config = config['config']

    def sync(self):
        """Synchronise the config."""
        with open_and_save(self.config_path) as config:
            config['config'] = self._config


class YunConfig(Config, metaclass=SingletonMeta):
    """The master config manager."""

    def __init__(self, path: str):
        """Create the manager from a master config file."""
        super(YunConfig, self).__init__(path)

    @property
    def mongo_host(self) -> str:
        """The URL to the database."""
        return self._config['mongo']['host']

    @property
    def mongo_port(self) -> int:
        return self._config['mongo']['port']

    @property
    def yun_host(self):
        return self._config['yun']['host']

    @property
    def yun_intermediate_path(self):
        return self._config['yun']['intermediate_path']


YUN_CONFIG = YunConfig(DEFAULT_YUN_CONFIG_PATH)
