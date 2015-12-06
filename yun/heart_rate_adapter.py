#!/usr/env/bin python
# -*- encoding: utf-8 -*-

"""
Heart rate sensor adapter.
"""

import random
import time
from typing import Optional

from requests import get

from yun.config import YUN_CONFIG

__author__ = 'Nb'

# request url
REQUEST_URL = YUN_CONFIG.yun_host + '/data/'


class HeartRateSensorState:
    """Heart rate sensor state."""
    DATA_SOURCE_ABSENT = 0
    COLLECTING_DATA = 1
    REPORTING_DATA = 2


class HeartRateData:
    """Packed heart rate data."""

    def __init__(self, raw_json: dict):
        """Parse the raw JSON response."""
        self.state = raw_json['state']
        self.micro_period_rate = raw_json['micro_period_rate']
        self.report_period_rate = raw_json['report_period_rate']

    @property
    def heart_rate(self) -> Optional[int]:
        """Reported heart rate."""
        if self.state == HeartRateSensorState.REPORTING_DATA:
            return self.report_period_rate
        return None

    @property
    def json(self):
        """Get the JSON representation."""
        return {
            'state': self.state,
            'micro_period_rate': self.micro_period_rate,
            'report_period_rate': self.report_period_rate
        }


# assistant timer for the fake heart rate for local test
_last_time = time.time()
_state_switch_map = {0: 1, 1: 2, 2: 0}
_current_state = 0
_switch_period = 10  # in seconds


def get_heart_rate(fake=False):
    """
    Get heart rate.
    @param fake: Generate fake data for local test or not.
    """
    if fake:
        global _last_time, _current_state
        if time.time() - _last_time > _switch_period:
            _current_state = _state_switch_map[_current_state]
            _last_time = time.time()
        return HeartRateData({
            'state': _current_state,
            'micro_period_rate': 72,
            'report_period_rate': random.randint(72, 88)
        })
    response = get(REQUEST_URL)
    if response.status_code == 200:
        return HeartRateData(response.json())
    else:
        raise ConnectionError('Cannot retrieve heart rate data')
