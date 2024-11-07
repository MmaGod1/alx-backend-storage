#!/usr/bin/env python3
"""An expiring web cache and tracker"""
import redis
from typing import Callable
import requests
from functools import wraps


def page_decor(func: Callable) -> Callable:
    """A decorator tracking how manny times a url is accessed."""
    connect = redis.Redis()
    connect.flushdb()

    @wraps(func)
    def wrapper(*args, **kwargs):
        url = args[0]  # Assuming the first argument is the URL
        url_page_count = f"count:{url}"  # Key for counting the number of accesses
        url_page_list = f"list:{url}"    # Key for storing the list of accessed URLs

        # Increment the count for the specific URL
        count = connect.incr(url_page_count)  # Increment the access count
        connect.expire(url_page_count, 10)  # Set expiration time of 10 seconds

        # Store the URL in the list
        connect.rpush(url_page_list, url)
        connect.expire(url_page_list, 10)  # Set expiration time for the list

        # Print out the current count and list in Redis for debugging
        print(f"URL access count for {url}: {count}")
        print(f"List of accessed URLs: {connect.lrange(url_page_list, 0, -1)}")

        return func(*args, **kwargs)  # Call the decorated function

    return wrapper


@page_decor
def get_page(url: str) -> str:
    """Requests for a page"""
    page = requests.get(url)
    return page.text


# Call the decorated function
try1 = get_page('http://slowwly.robertomurray.co.uk')

# Print the page content (this is just for testing)
print(try1)
