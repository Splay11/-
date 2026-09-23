from collections import OrderedDict


class TTL_LRU:
    """带 TTL 的 LRU：满时先淘汰过期，再淘汰最久未使用。"""

    def __init__(self, capacity: int):
        self.cap = capacity
        # key -> (value, expire_time)；OrderedDict 维护 LRU 顺序（末尾最新）
        self.mp = OrderedDict()

    def _expired(self, key: int, ts: int) -> bool:
        return self.mp[key][1] <= ts

    def _evict(self, ts: int):
        # 优先淘汰已过期（按 LRU 从旧到新找第一个过期）
        for k in list(self.mp.keys()):
            if self._expired(k, ts):
                del self.mp[k]
                return
        # 无过期则淘汰最久未使用
        self.mp.popitem(last=False)

    def put(self, key: int, value: int, ttl: int, ts: int):
        expire = ts + ttl
        if key in self.mp:
            del self.mp[key]
            self.mp[key] = (value, expire)
            return
        if len(self.mp) >= self.cap:
            self._evict(ts)
        self.mp[key] = (value, expire)

    def get(self, key: int, ts: int) -> int:
        if key not in self.mp:
            return -1
        if self._expired(key, ts):
            del self.mp[key]
            return -1
        val, exp = self.mp.pop(key)
        # 命中则视为最近使用
        self.mp[key] = (val, exp)
        return val


def main():
    capacity, q = map(int, input().split())
    cache = TTL_LRU(capacity)
    for _ in range(q):
        parts = input().split()
        if parts[0] == "put":
            key, value, ttl, ts = map(int, parts[1:])
            cache.put(key, value, ttl, ts)
        else:
            key, ts = map(int, parts[1:])
            print(cache.get(key, ts))


if __name__ == "__main__":
    main()
