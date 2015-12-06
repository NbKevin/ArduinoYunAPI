#!/usr/env/bin python
# -*- encoding: utf-8 -*-

"""
Fetch readings and store them into the database.
"""

from yun.adapter import read_pin
from yun.config import YUN_CONFIG
from yun.database import SensorReadingDatabase

__author__ = 'Nb'

SENSOR_DB = SensorReadingDatabase(YUN_CONFIG.mongo_host, YUN_CONFIG.mongo_port, 'astra', 'sensor')

while True:
    response = read_pin(1)
    sensor, reading = response['pin'], response['value']
    # SENSOR_DB.add_entry(sensor, reading)
    print('Retrieved %s from sensor on pin %s' % (reading, sensor))
