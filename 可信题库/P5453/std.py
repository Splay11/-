# -*- coding: utf-8 -*-
from collections import deque
from typing import Deque, Dict, List, Optional, Set


class ParkingLane:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.lane: List[int] = []  # stack, end = front/exit
        self.wait: Deque[int] = deque()
        self.in_lane: Set[int] = set()
        self.in_wait: Set[int] = set()
        self.hist: List[tuple] = []  # ('arrive', carId, 'lane'|'wait') / ('admit', carId) / ('depart', carId)

    def arrive(self, carId: int) -> bool:
        if carId in self.in_lane or carId in self.in_wait:
            return False
        if len(self.lane) < self.cap:
            self.lane.append(carId)
            self.in_lane.add(carId)
            self.hist.append(("arrive", carId, "lane"))
        else:
            self.wait.append(carId)
            self.in_wait.add(carId)
            self.hist.append(("arrive", carId, "wait"))
        return True

    def admit(self) -> bool:
        if not self.wait or len(self.lane) >= self.cap:
            return False
        carId = self.wait.popleft()
        self.in_wait.remove(carId)
        self.lane.append(carId)
        self.in_lane.add(carId)
        self.hist.append(("admit", carId))
        return True

    def depart(self, carId: int) -> int:
        if carId not in self.in_lane:
            return -1
        temp: List[int] = []
        moved = 0
        while self.lane and self.lane[-1] != carId:
            x = self.lane.pop()
            temp.append(x)
            moved += 1
        # pop target
        self.lane.pop()
        self.in_lane.remove(carId)
        # restore
        while temp:
            x = temp.pop()
            self.lane.append(x)
        self.hist.append(("depart", carId))
        return moved

    def undo(self) -> bool:
        if not self.hist:
            return False
        rec = self.hist.pop()
        kind = rec[0]
        if kind == "arrive":
            carId, where = rec[1], rec[2]
            if where == "lane":
                if not self.lane or self.lane[-1] != carId:
                    # 状态被后续操作破坏则视为失败，但历史已弹；为严谨应保证不会发生
                    self.hist.append(rec)
                    return False
                self.lane.pop()
                self.in_lane.remove(carId)
            else:
                if carId not in self.in_wait:
                    self.hist.append(rec)
                    return False
                self.wait.remove(carId)
                self.in_wait.remove(carId)
            return True
        if kind == "admit":
            carId = rec[1]
            if not self.lane or self.lane[-1] != carId:
                self.hist.append(rec)
                return False
            self.lane.pop()
            self.in_lane.remove(carId)
            self.wait.appendleft(carId)
            self.in_wait.add(carId)
            return True
        if kind == "depart":
            carId = rec[1]
            if carId in self.in_lane or carId in self.in_wait:
                self.hist.append(rec)
                return False
            if len(self.lane) >= self.cap:
                self.hist.append(rec)
                return False
            self.lane.append(carId)
            self.in_lane.add(carId)
            return True
        return False

    def front(self) -> int:
        return self.lane[-1] if self.lane else -1

    def waiting(self) -> int:
        return len(self.wait)

    def size(self) -> int:
        return len(self.lane)
