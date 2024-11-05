#!/usr/bin/env python3
"""Module to define redis Python classes"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator that would count how many times a method is called."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """Store an instance of the Redis client as a private."""
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Takes a data argument and returns a string."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
           fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
           Take a key string argument and an optional Callable argument named fn.
           This callable will be used to convert the data back to the desired format.
        """
        value = self._redis.get(key)
        if fn:
            return fn(value)
        return value
               
    def get_str(self, key: str) -> str:
      """Automatically parametrize Cache.get to a str."""
      return self._redis.get(key).decode("utf-8")
        
    def get_int(self, key: int) -> int:
      """Automatically parametrize Cache.get to an int"""
      return self.get(key, fn=int)
