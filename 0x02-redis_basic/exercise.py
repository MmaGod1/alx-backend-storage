#!/usr/bin/env python3
"""Module to define redis Python classes"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator that would count how many times a method is called."""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Store the history of inputs and outputs for a particular function."""
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        return output
    return wrapper


def replay(method: Callable):
    """Display the history of calls for a particular function."""
    # Get the cache instance
    cache_instance = method.__self__
    
    # Retrieve the input and output keys
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"
    
    # Retrieve the inputs and outputs from Redis
    inputs = cache_instance._redis.lrange(input_key, 0, -1)
    outputs = cache_instance._redis.lrange(output_key, 0, -1)
    
    # Display the history
    print(f"{method.__qualname__} was called {len(inputs)} times:")
    
    # Loop through inputs and outputs, using zip to pair them
    for input_data, output_data in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{input_data.decode()}) -> {output_data.decode()}")

class Cache:
    """Store an instance of the Redis client as a private."""
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Takes a data argument and returns a string."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
            Take a key string and an optional Callable argument named fn.
            The callable will be used to convert the data to a desired format.
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
