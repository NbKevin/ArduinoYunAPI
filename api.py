#!/usr/env/bin python
# -*- encoding: utf-8 -*-

"""
RESTful APIs.
"""

from flask.ext.restful import Resource, reqparse

from yun.adapter import read_pin
from yun.heart_rate_adapter import get_heart_rate

__author__ = 'Nb'


# noinspection PyMethodMayBeStatic,PyAbstractClass
class YunRealtimeReadingsAPI(Resource):
    """Retrieve realtime yun readings."""

    def get(self):
        """Get readings from a certain pin."""
        parser = reqparse.RequestParser()
        parser.add_argument('analogue', type=bool, help='Pin type')
        parser.add_argument('pin', type=int, help='Pin number', required=True)
        args = parser.parse_args()
        return read_pin(args['pin'], args['analogue'])


# noinspection PyMethodMayBeStatic,PyAbstractClass
class YunRealtimeHeartRateAPI(Resource):
    """Retrieve realtime heart rate from Arduino Yun."""

    def get(self):
        """Get heart rate data."""
        heart_rate = get_heart_rate(fake=True)
        print(heart_rate.json)
        return heart_rate.json
