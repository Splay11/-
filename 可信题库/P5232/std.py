from typing import Dict, List, Tuple


class MemMgmtSys:
    def __init__(self, num: int):
        self.n = num
        self.page: List[int] = [-1] * num
        self.info: Dict[int, Tuple[int, int]] = {}

    def _find(self, size: int) -> int:
        i = 0
        while i < self.n:
            if self.page[i] != -1:
                i += 1
                continue
            j = i
            while j < self.n and self.page[j] == -1:
                j += 1
            if j - i >= size:
                return i
            i = j
        return -1

    def _defrag(self) -> None:
        items = [(sz, pid) for pid, (_st, sz) in self.info.items()]
        items.sort()
        self.page = [-1] * self.n
        self.info.clear()
        used = sum(sz for sz, _ in items)
        pos = self.n - used
        for sz, pid in items:
            for k in range(sz):
                self.page[pos + k] = pid
            self.info[pid] = (pos, sz)
            pos += sz

    def processMemAlloc(self, processId: int, size: int) -> int:
        st = self._find(size)
        if st < 0:
            self._defrag()
            st = self._find(size)
            if st < 0:
                return -1
        for k in range(size):
            self.page[st + k] = processId
        self.info[processId] = (st, size)
        return st

    def processMemFree(self, processId: int) -> None:
        st, sz = self.info.pop(processId)
        for k in range(sz):
            self.page[st + k] = -1

    def processMemQuery(self, processId: int) -> int:
        return self.info[processId][0]
