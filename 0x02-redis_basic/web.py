import requests
import hashlib
import redis
from functools import wraps
import time

# Create a Redis connection
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def cache_page(func):
    @wraps(func)
    def wrapper(url):
        cache_key = f'cache:{url}'
        count_key = f'count:{url}'

        # Check if the page content is cached
        cached_content = redis_client.get(cache_key)
        if cached_content:
            # If cached, increment the access count and return the cached content
            redis_client.incr(count_key)
            return cached_content.decode('utf-8')

        # If not cached, fetch the content from the URL
        response = requests.get(url)
        page_content = response.text

        # Cache the page content with a 10-second expiration time
        redis_client.setex(cache_key, 10, page_content)

        # Initialize the access count to 1
        redis_client.set(count_key, 1)

        return page_content

    return wrapper

@cache_page
def get_page(url):
    return requests.get(url).text

if __name__ == '__main__':
    url = 'http://google.com'

    # Access the URL multiple times to test caching
    for _ in range(5):
        content = get_page(url)
        print(f"Content length: {len(content)}")

    # Wait for 10 seconds to allow the cache to expire
    time.sleep(10)

    # Access the URL after the cache has expired
    content = get_page(url)
    print(f"Content length: {len(content}")

    # Check how many times the URL was accessed
    access_count = redis_client.get(f'count:{url}')
    print(f"URL access count: {access_count.decode('utf-8')}")

