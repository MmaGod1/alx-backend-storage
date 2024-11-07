import redis
from typing import Callable
import requests
from functools import wraps
import time

# Redis connection is now accessible globally
connect = redis.Redis()

def page_decor(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        url = args[0]  # Assuming the first argument is the URL
        url_page_count = f"count:{url}"  # Key for counting the number of accesses
        url_page_list = f"list:{url}"    # Key for storing the list of accessed URLs

        # Initialize the count to 0 if it doesn't exist
        if not connect.exists(url_page_count):
            connect.set(url_page_count, 0)

        # Increment the count for the specific URL
        count = connect.incr(url_page_count)  # Increment the access count
        connect.expire(url_page_count, 10)  # Set expiration time of 10 seconds
        
        # Store the URL in the list
        connect.rpush(url_page_list, url)
        connect.expire(url_page_list, 10)  # Set expiration time for the list
        
        return func(*args, **kwargs)  # Call the decorated function
    
    return wrapper

@page_decor
def get_page(url: str) -> str:
    page = requests.get(url)
    return page.text

# Call the decorated function once
get_page('http://slowwly.robertomurray.co.uk')

# Function to check if the URL count is still cached in Redis
def check_cache(url: str) -> None:
    url_page_count = f"count:{url}"
    
    # Check if the key still exists in Redis
    if connect.exists(url_page_count):
        print(f"Redis count for URL still exists: {connect.get(url_page_count)}")
    else:
        print("Redis count for URL has expired and is no longer cached.")

# Wait for 10 seconds before checking
time.sleep(10)  # You can manually wait 10 seconds or call this check after the delay

# Check cache after 10 seconds
check_cache('http://slowwly.robertomurray.co.uk')
