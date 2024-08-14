#!/usr/bin/env python3
"""Module for utilizing the NoSQL data storage Redis basic"""
import redis
import uuid


class Cache:
    """Class that manages data storage in Redis database"""
    def __init__(self) -> None:
        """Initilizing cache instance and clear previous data"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Storing a value in database and returns generated key"""
        randomKey = str(uuid.uuid4())
        self._redis.set(randomKey, data)
        return randomKey
