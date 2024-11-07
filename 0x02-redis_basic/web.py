import redis
from typing import Callable
import requests
from functools import wraps

def page_decor(func: Callable) -> Callable:
    connect = redis.Redis()

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


# Call the decorated function
try1 = get_page('http://slowwly.robertomurray.co.uk')

# Print the page content
print(try1)

# Check the count in Redis for testing (optional, to verify it's incremented)
connect = redis.Redis()
url_page_count = "count:http://google.com"
print(connect.get(url_page_count))  # Should print the incremented count
