#!/usr/bin/env python3
"""An expiring web cache and tracker"""
import redis
import requests
from functools import wraps

r = redis.Redis(host='localhost', port=6379, db=0)

def cache_page(func):
    """
    A decorator to cache the result of a function and track access count.
    """
    @wraps(func)
    def wrapper(url: str):
        cache_key = f"page:{url}"
        cached_page = r.get(cache_key)
        
        if cached_page:
            return cached_page.decode('utf-8')
        
        page = func(url)
        r.setex(cache_key, 10, page)  # Cache with 10-second expiration
        r.incr(f"count:{url}")  # Increment the access count
        
        return page
    return wrapper

@cache_page
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL.
    """
    response = requests.get(url)
    return response.text
