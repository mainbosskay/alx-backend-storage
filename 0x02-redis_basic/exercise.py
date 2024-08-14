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


def call_history(method: Callable) -> Callable:
    """Decorator that tracks details of call of method within Cache"""
    @wraps(method)
    def handler(self, *args, **kwargs) -> Any:
        """Storing method call details in Redis and returns output"""
        key_input = f"{method.__qualname__}:inputs"
        key_output = f"{method.__qualname__}:outputs"
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(key_input, str(args))
        methodResult = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(key_output, methodResult)
        return methodResult
    return handler


def replay(method: Callable) -> None:
    """Displaying call history for method decorated"""
    if method is None or not hasattr(method, "__self__"):
        return
    instRedis = getattr(method.__self__, "_redis", None)
    if not isinstance(instRedis, redis.Redis):
        return
    methodName = method.__qualname__
    key_input = f"{methodName}:inputs"
    key_output = f"{methodName}:outputs"
    methodCallCount = 0
    if instRedis.exists(methodName) != 0:
        methodCallCount = int(instRedis.get(methodName))
    print(f"{methodName} was called {methodCallCount} times:")
    inputValues = instRedis.lrange(key_input, 0, -1)
    outputValues = instRedis.lrange(key_output 0, -1)
    for inputVal, outputVal in zip(inputValues, outputValues):
        print(f"{methodName}(*{inputVal.decode('utf-8')}) -> {outputVal}")


class Cache:
    """Class that manages data storage in Redis database"""
    def __init__(self) -> None:
        """Initilizing cache instance and clear previous data"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores a value in database and returns generated key"""
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
