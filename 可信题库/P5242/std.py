from typing import Dict, List, Tuple


class ParkingLot:
    def __init__(self, n: int):
        self.n = n
        # 每个车位上的占用区间列表
        self.spots: List[List[Tuple[int, int]]] = [[] for _ in range(n)]
        # carId -> (spot, start, end)
        self.car: Dict[int, Tuple[int, int, int]] = {}

    def _conflict(self, intervals: List[Tuple[int, int]], start: int, end: int) -> bool:
        # 半开区间 [start,end) 与 [s,e) 相交
        for s, e in intervals:
            if start < e and s < end:
                return True
        return False

    def reserve(self, carId: int, start: int, end: int) -> int:
        if carId in self.car or start >= end:
            return -1
        for spot in range(self.n):
            if not self._conflict(self.spots[spot], start, end):
                self.spots[spot].append((start, end))
                self.car[carId] = (spot, start, end)
                return spot
        return -1

    def cancel(self, carId: int) -> bool:
        if carId not in self.car:
            return False
        spot, start, end = self.car.pop(carId)
        self.spots[spot].remove((start, end))
        return True

    def spotOf(self, carId: int) -> int:
        if carId not in self.car:
            return -1
        return self.car[carId][0]

    def busyCount(self, time: int) -> int:
        cnt = 0
        for _, start, end in self.car.values():
            if start <= time < end:
                cnt += 1
        return cnt
