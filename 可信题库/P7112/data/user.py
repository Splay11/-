class ShardLeaseManager:
    def __init__(self, shardCount: int, maxHold: int):
        pass

    def acquire(self, clientId: int, shardId: int, now: int, ttl: int) -> bool:
        return False

    def renew(self, clientId: int, shardId: int, now: int, ttl: int) -> bool:
        return False

    def release(self, clientId: int, shardId: int, now: int) -> bool:
        return False

    def owner(self, shardId: int, now: int) -> int:
        return -1

    def heldCount(self, clientId: int, now: int) -> int:
        return -1
