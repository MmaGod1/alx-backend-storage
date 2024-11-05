#!/usr/bin/env python3
"""Module to define redis Python classes"""
import redis
import uuid
from typing import Union

class Cache:
    """Store an instance of the Redis client as a private."""
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Takes a data argument and returns a string."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
        
