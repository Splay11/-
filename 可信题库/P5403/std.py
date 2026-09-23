import heapq


class MicQueue:
    def __init__(self):
        self.heat = {}
        self.heap = []

    def enroll(self, songId: int, heat: int) -> bool:
        if songId in self.heat:
            return False
        self.heat[songId] = heat
        heapq.heappush(self.heap, (-heat, songId))
        return True

    def nextPlay(self) -> int:
        while self.heap:
            h, sid = heapq.heappop(self.heap)
            h = -h
            if self.heat.get(sid) == h:
                del self.heat[sid]
                return sid
        return -1

    def boost(self, songId: int, addHeat: int) -> bool:
        if songId not in self.heat:
            return False
        self.heat[songId] += addHeat
        heapq.heappush(self.heap, (-self.heat[songId], songId))
        return True

    def cancel(self, songId: int) -> bool:
        if songId not in self.heat:
            return False
        del self.heat[songId]
        return True

    def waiting(self) -> int:
        return len(self.heat)
