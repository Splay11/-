from typing import Dict, List


class LogChunk:
    def __init__(self, mid: int, idx: int) -> None:
        self.mid = mid
        self.idx = idx
        self.sz = 0


class FileLogger:
    def __init__(self, fileCap: int, totalCap: int) -> None:
        self.cap = fileCap
        self.quota = totalCap
        self.files: List[LogChunk] = []
        self.cur: Dict[int, LogChunk] = {}
        self.seq: Dict[int, int] = {}

    def totalSize(self) -> int:
        return sum(f.sz for f in self.files)

    def _drop_oldest(self) -> None:
        f = self.files.pop(0)
        if self.cur.get(f.mid) is f:
            del self.cur[f.mid]

    def putLog(self, mid: int, nbytes: int) -> int:
        while self.totalSize() + nbytes > self.quota:
            self._drop_oldest()
        cur = self.cur.get(mid)
        if cur is None or cur.sz + nbytes > self.cap:
            self.seq[mid] = self.seq.get(mid, 0) + 1
            cur = LogChunk(mid, self.seq[mid])
            self.files.append(cur)
            self.cur[mid] = cur
        cur.sz += nbytes
        return cur.sz

    def listFiles(self) -> List[List[int]]:
        return [[f.mid, f.idx, f.sz] for f in self.files]
