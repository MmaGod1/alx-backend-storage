#!/usr/bin/env python3
import redis
import requests
from typing import Callable
from functools import wraps

# Redis connection
connect = redis.Redis()

def page_decor(func: Callable) -> Callable:
    """Decorator for tracking URL access count and caching the result."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        url = args[0]  # URL is expected as the first argument
        url_page_count = f"count:{url}"  # Redis key for access count
        
        # Initialize the count to 0 if it doesn't exist
        if not connect.exists(url_page_count):
            connect.set(url_page_count, 0)
        
        # Increment the access count for the URL
        connect.incr(url_page_count)
        
        # Set expiration of the count key to 10 seconds
        connect.expire(url_page_count, 10)
        
        # Call the original function
        return func(*args, **kwargs)
    
    return wrapper

@page_decor
def get_page(url: str) -> str:
    """Fetches the page content from the given URL."""
    response = requests.get(url)
    return response.text

"""
# Call the decorated function for testing
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://google.com"
    content = get_page(url)  # This will trigger the decorator
    print(content)  # Print the page content

    # After 10 seconds, the cache will expire
    import time
    time.sleep(10)

    # Test again after expiration
    print(get_page(url))  # This should be a fresh call since the cache expired
"""
