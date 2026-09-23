class TTLCache:
    def __init__(self, capacity: int):
        pass

    def put(self, key: int, value: int, expireAt: int) -> None:
        pass

    def get(self, key: int, now: int) -> int:
        return -1

    def purge(self, now: int) -> int:
        return 0

    def size(self) -> int:
        return 0
