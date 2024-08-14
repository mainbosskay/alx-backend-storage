#!/usr/bin/env python3
"""Module for utilizing the NoSQL data storage Redis basic"""
import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator that tracks number of calls made to methos within Cache"""
    @wraps(method)
    def handler(self, *args, **kwargs) -> Any:
        """Incrementing call counter for decorated method to invokes it"""
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return handler


class Cache:
    """Class that manages data storage in Redis database"""
    def __init__(self) -> None:
        """Initilizing cache instance and clear previous data"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Storing a value in database and returns generated key"""
        randomKey = str(uuid.uuid4())
        self._redis.set(randomKey, data)
        return randomKey

    def get(self, key: str, fn: Callable = None)\
            -> Union[str, bytes, int, float]:
        """Getting and returns value from database using a key"""
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """Getting and returns value from database as a string"""
        return self.get(key, lambda k: k.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Getting and returns value from database as an integer"""
        return self.get(key, lambda k: int(k))
