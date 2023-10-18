#!/usr/bin/env python3
"""Redis and Python exercise"""
import redis
import uuid
from typing import Union, Callable


class Cache:

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable[[bytes], any] = None)/
          -> Union[str, bytes, int, float, None]:
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        return self.get(key, fn=lambda data: data.decode("utf-8"))

    def get_int(self, key: str) -> int:
        return self.get(key, fn=int)
