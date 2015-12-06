#!/usr/env/bin python
# -*- encoding: utf-8 -*-

"""
Database related business.
"""

from datetime import datetime, timezone
from typing import Union

from pymongo import MongoClient

from yun.utilities import SingletonMeta

__author__ = 'Nb'


class Database:
    """Database manager."""

    def __init__(self, mongo_host: str, mongo_port: int, db_name: str):
        """Initialise the database from a Mongo url and
        the name of the database desired."""
        self._mongo = MongoClient(mongo_host, mongo_port)
        self._db = self._mongo.get_database(db_name)


class SensorReadingDatabase(Database, metaclass=SingletonMeta):
    """Database of readings from sensors."""

    def __init__(self, mongo_host: str, mongo_port: int, db_name: str, collection_name: str):
        """Initialise the database from a Mongo url,
        the name of the database and the collection
        desired."""
        super().__init__(mongo_host, mongo_port, db_name)
        self._collection = self._db.get_collection(collection_name)

    def add_entry(self, sensor_name: str, sensor_reading: Union[int, float, str], local_timestamp: int = None):
        """
        Add an entry for new readings from the sensor.
        The current UTC time is used by default while
        a custom local UNIX timestamp can be passed in
        manually.

        @param sensor_name: The name of the sensor.
        @param sensor_reading: The reading of the sensor.
        @param local_timestamp: UNIX timestamp in local time.
        """
        local_time = datetime.now() if local_timestamp is None \
            else datetime.utcfromtimestamp(local_timestamp)
        entry = {
            'sensor': sensor_name,
            'reading': sensor_reading,
            'time': local_time.now(timezone.utc)
        }
        self._collection.insert_one(entry)
