#!/usr/env/bin python
# -*- encoding: utf-8 -*-

"""
Heart rate sensor adapter.
"""

import random
import time
from threading import Thread
from typing import Optional

from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectTimeout, ReadTimeout
from requests.packages.urllib3.exceptions import NewConnectionError

from yun.config import YUN_CONFIG

__author__ = 'Nb'

# request url
REQUEST_URL = 'http://' + YUN_CONFIG.yun_host + '/' + YUN_CONFIG.yun_intermediate_path + '/heartrate/'

# retry limited session
_patched_session = Session()
_patched_session.mount('http://', HTTPAdapter(max_retries=1))


class HeartRateSensorState:
    """Heart rate sensor state."""
    DATA_SOURCE_ABSENT = 0
    COLLECTING_DATA = 1
    REPORTING_DATA = 2
    SENSOR_ABSENT = -1


class HeartRateData:
    """Packed heart rate data."""

    def __init__(self, raw_json: dict):
        """Parse the raw JSON response."""
        self.state = raw_json['state']
        self.raw_heart_rate = raw_json['hr']

    @property
    def heart_rate(self) -> Optional[int]:
        """Reported heart rate."""
        if self.state == HeartRateSensorState.REPORTING_DATA:
            return self.raw_heart_rate
        return None

    @property
    def json(self):
        """Get the JSON representation."""
        return {
            'state': self.state,
            'hr': self.heart_rate
        }


# assistant timer for the fake heart rate for local test
_last_time = time.time()
_state_switch_map = {0: 1, 1: 2, 2: 0}
_current_state = 0
_switch_period = 10  # in seconds

# global heart rate instance
_sensor_absent_heart_rate_placeholder = HeartRateData({
    'state': HeartRateSensorState.SENSOR_ABSENT,
    'hr': 0.0
})
_heart_rate = _sensor_absent_heart_rate_placeholder

# background thread indicator
_keep_running = True


class _HeartRateThread(Thread):
    """The thread for getting heart rate in the background."""

    def __init__(self):
        super().__init__()

    def run(self):
        global _heart_rate, _keep_running
        while _keep_running:
            try:
                response = _patched_session.get(REQUEST_URL, timeout=(3, 5))
                if response.status_code == 200:
                    _heart_rate = HeartRateData(response.json())
            except (ConnectTimeout, ReadTimeout, ConnectionError, NewConnectionError):
                _heart_rate = _sensor_absent_heart_rate_placeholder
            print('%s: %s' % (self.getName(), _heart_rate.json))
            time.sleep(.25)


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
            'hr': random.randint(60, 90)
        })
    return _heart_rate
