class LeaseManager:
    def __init__(self, ttl: int):
        pass
    def acquire(self, resourceId: int, nodeId: int, time: int) -> bool:
        return False
    def renew(self, resourceId: int, nodeId: int, time: int) -> bool:
        return False
    def release(self, resourceId: int, nodeId: int) -> bool:
        return False
    def holder(self, resourceId: int, time: int) -> int:
        return -1
    def aliveCount(self, time: int) -> int:
        return 0
