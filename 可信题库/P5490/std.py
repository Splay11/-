from typing import List


class ParcelSlots:
    def __init__(self, n: int):
        self.n = n
        self.slot: List[int] = [0] * n
        self.cnt = 0

    def put(self, i: int, w: int) -> bool:
        if i < 1 or i > self.n or w <= 0 or self.slot[i - 1] != 0:
            return False
        self.slot[i - 1] = w
        self.cnt += 1
        return True

    def take(self, i: int) -> int:
        if i < 1 or i > self.n or self.slot[i - 1] == 0:
            return 0
        w = self.slot[i - 1]
        self.slot[i - 1] = 0
        self.cnt -= 1
        return w

    def moveRight(self, i: int) -> bool:
        if i < 1 or i >= self.n or self.slot[i - 1] == 0 or self.slot[i] != 0:
            return False
        self.slot[i] = self.slot[i - 1]
        self.slot[i - 1] = 0
        return True

    def occupied(self) -> int:
        return self.cnt
