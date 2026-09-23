# -*- coding: utf-8 -*-
from typing import Dict, Tuple


class TTLCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.data: Dict[int, Tuple[int, int]] = {}  # key -> (value, expireAt)

    def put(self, key: int, value: int, expireAt: int) -> None:
        self.data[key] = (value, expireAt)
        if len(self.data) > self.capacity:
            # 淘汰：过期时刻最早，相同时键更小
            victim = min(self.data.items(), key=lambda kv: (kv[1][1], kv[0]))[0]
            del self.data[victim]

    def get(self, key: int, now: int) -> int:
        if key not in self.data:
            return -1
        value, expireAt = self.data[key]
        if now >= expireAt:
            return -1
        return value

    def purge(self, now: int) -> int:
        dead = [k for k, (_, exp) in self.data.items() if now >= exp]
        for k in dead:
            del self.data[k]
        return len(dead)

    def size(self) -> int:
        return len(self.data)
