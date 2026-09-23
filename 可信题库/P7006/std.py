# -*- coding: utf-8 -*-
"""P7006 ClusterPool 标程：哈希表模拟 best-fit 调度。"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple


class ClusterPool:
    def __init__(self) -> None:
        # nodeId -> capacity / used / 其上任务数
        self.cap: Dict[int, int] = {}
        self.used: Dict[int, int] = {}
        self.job_cnt: Dict[int, int] = {}
        # jobId -> (nodeId, size)
        self.jobs: Dict[int, Tuple[int, int]] = {}

    def addNode(self, nodeId: int, capacity: int) -> bool:
        if nodeId in self.cap or capacity <= 0:
            return False
        self.cap[nodeId] = capacity
        self.used[nodeId] = 0
        self.job_cnt[nodeId] = 0
        return True

    def removeNode(self, nodeId: int) -> bool:
        if nodeId not in self.cap:
            return False
        if self.job_cnt[nodeId] > 0:
            return False
        del self.cap[nodeId]
        del self.used[nodeId]
        del self.job_cnt[nodeId]
        return True

    def submit(self, jobId: int, size: int) -> int:
        if jobId in self.jobs or size <= 0:
            return -1
        best_id = -1
        best_rem = None  # type: Optional[int]
        for nid, capacity in self.cap.items():
            rem = capacity - self.used[nid]
            if rem < size:
                continue
            # best-fit：剩余更小优先；并列取更小 nodeId
            if best_rem is None or rem < best_rem or (rem == best_rem and nid < best_id):
                best_rem = rem
                best_id = nid
        if best_id < 0:
            return -1
        self.used[best_id] += size
        self.job_cnt[best_id] += 1
        self.jobs[jobId] = (best_id, size)
        return best_id

    def kill(self, jobId: int) -> bool:
        info = self.jobs.pop(jobId, None)
        if info is None:
            return False
        nid, size = info
        self.used[nid] -= size
        self.job_cnt[nid] -= 1
        return True

    def usedOf(self, nodeId: int) -> int:
        if nodeId not in self.cap:
            return -1
        return self.used[nodeId]

    def freeOf(self, nodeId: int) -> int:
        if nodeId not in self.cap:
            return -1
        return self.cap[nodeId] - self.used[nodeId]

    def jobNode(self, jobId: int) -> int:
        info = self.jobs.get(jobId)
        if info is None:
            return -1
        return info[0]


def run_ops(ops: List[str]) -> List[str]:
    import re

    outs: List[str] = []
    obj: Optional[ClusterPool] = None
    for line in ops:
        line = line.strip()
        if not line:
            continue
        if line == "ClusterPool()":
            obj = ClusterPool()
            outs.append("null")
        elif line.startswith("addNode("):
            m = re.fullmatch(r"addNode\((-?\d+),\s*(-?\d+)\)", line)
            if not m:
                raise ValueError(line)
            assert obj is not None
            outs.append("true" if obj.addNode(int(m.group(1)), int(m.group(2))) else "false")
        elif line.startswith("removeNode("):
            m = re.fullmatch(r"removeNode\((-?\d+)\)", line)
            if not m:
                raise ValueError(line)
            assert obj is not None
            outs.append("true" if obj.removeNode(int(m.group(1))) else "false")
        elif line.startswith("submit("):
            m = re.fullmatch(r"submit\((-?\d+),\s*(-?\d+)\)", line)
            if not m:
                raise ValueError(line)
            assert obj is not None
            outs.append(str(obj.submit(int(m.group(1)), int(m.group(2)))))
        elif line.startswith("kill("):
            m = re.fullmatch(r"kill\((-?\d+)\)", line)
            if not m:
                raise ValueError(line)
            assert obj is not None
            outs.append("true" if obj.kill(int(m.group(1))) else "false")
        elif line.startswith("usedOf("):
            m = re.fullmatch(r"usedOf\((-?\d+)\)", line)
            if not m:
                raise ValueError(line)
            assert obj is not None
            outs.append(str(obj.usedOf(int(m.group(1)))))
        elif line.startswith("freeOf("):
            m = re.fullmatch(r"freeOf\((-?\d+)\)", line)
            if not m:
                raise ValueError(line)
            assert obj is not None
            outs.append(str(obj.freeOf(int(m.group(1)))))
        elif line.startswith("jobNode("):
            m = re.fullmatch(r"jobNode\((-?\d+)\)", line)
            if not m:
                raise ValueError(line)
            assert obj is not None
            outs.append(str(obj.jobNode(int(m.group(1)))))
        else:
            raise ValueError(line)
    return outs


if __name__ == "__main__":
    import sys

    lines = sys.stdin.read().split("\n")
    print("\n".join(run_ops(lines)))
