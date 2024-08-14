#!/usr/bin/env python3
"""Module for Redis database with tools for request cache and track"""
import redis
import requests
from functools import wraps
from typing import Callable


redisInst = redis.Redis()


def cache_data(method: Callable) -> Callable:
    """Decorator cache fetched data and track request counts"""
    @wraps(method)
    def handler(url) -> str:
        """Handles caching output of decorated method"""
        redisInst.incr(f"count:{url}")
        value_after_cached = redisInst.get(f"result:{url}")
        if value_after_cached:
            return value_after_cached.decode("utf-8")
        value_before_cached = method(url)
        redisInst.setex(f"result:{url}", 10, value_before_cached)
        return value_before_cached
    return handler


@cache_data
def get_page(url: str) -> str:
    """Getting and returns URL content after cache response & tracks request"""
    return requests.get(url).text
