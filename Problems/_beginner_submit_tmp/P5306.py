class LeaseManager:
    def __init__(self, ttl: int):
        # ttl：租约时长；mp：资源 -> (持有者, 最近续约时刻)
        self.ttl = ttl
        self.mp = {}

    def _alive(self, resourceId: int, time: int) -> bool:
        # 有效条件：time < last + ttl
        if resourceId not in self.mp:
            return False
        _, last = self.mp[resourceId]
        return time < last + self.ttl

    def acquire(self, resourceId: int, nodeId: int, time: int) -> bool:
        # 被其他节点有效占用则失败
        if self._alive(resourceId, time):
            if self.mp[resourceId][0] != nodeId:
                return False
        # 空闲/过期/本人持有：写入或续约
        self.mp[resourceId] = (nodeId, time)
        return True

    def renew(self, resourceId: int, nodeId: int, time: int) -> bool:
        # 必须是当前有效持有者
        if not self._alive(resourceId, time):
            return False
        if self.mp[resourceId][0] != nodeId:
            return False
        self.mp[resourceId] = (nodeId, time)
        return True

    def release(self, resourceId: int, nodeId: int) -> bool:
        # 只要记录持有者匹配即可释放（过期也可清）
        if resourceId not in self.mp:
            return False
        if self.mp[resourceId][0] != nodeId:
            return False
        del self.mp[resourceId]
        return True

    def holder(self, resourceId: int, time: int) -> int:
        if not self._alive(resourceId, time):
            return -1
        return self.mp[resourceId][0]

    def aliveCount(self, time: int) -> int:
        # 统计仍有效的租约
        return sum(1 for rid in self.mp if self._alive(rid, time))
