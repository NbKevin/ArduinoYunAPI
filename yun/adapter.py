#!/usr/env/bin python
# -*- encoding: utf-8 -*-

"""
Yun API adapter for transporting data from Arduino Yun board.
"""

from requests import get, Response

from yun.config import YUN_CONFIG

__author__ = 'Nb'


def generate_arduino_url(pin: int, analogue=True, read=True, value: int = None):
    """
    Generate the API url for retrieving data from Arduino Yun.
    @param pin: Pin number.
    @param analogue: Analogue or digital.
    @param value: The value to write, ignored if read is True.
    @param read: Read or write.
    @return: The API url.
    """
    return '/'.join([
        'http:/',
        YUN_CONFIG.yun_host, YUN_CONFIG.yun_intermediate_path,
        'analogue' if analogue else 'digital',
        str(pin),
        str(value) if not read else ''
    ]).rstrip('/')


def _read_pin_result_parser(raw_response: Response) -> dict:
    """
    Parse the raw response of reading a pin.
    @param raw_response: Raw response.
    @return: The reading.
    """
    return raw_response.json()


def read_pin(pin: int, analogue=True, response_parser=_read_pin_result_parser):
    """
    Retrieve readings from a pin.
    @param pin: Pin number.
    @param analogue: Analogue or not.
    @param response_parser: The parser for parsing the raw response.
    @return: Readings from that pin.
    """
    request_url = generate_arduino_url(pin, analogue)
    response = get(request_url)
    if response.status_code != 200:
        raise ConnectionError('Cannot retrieve readings from %s pin %s' %
                              ('analogue' if analogue else 'digital', pin))
    return response_parser(response)
