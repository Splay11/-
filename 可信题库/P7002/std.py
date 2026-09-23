import heapq
from typing import Dict, List, Optional, Set


class JobQueueSys:
    def __init__(self):
        self.heap: List[tuple] = []  # (-priority, jobId)
        self.active: Set[int] = set()

    def submit(self, jobId: int, priority: int) -> bool:
        if jobId in self.active:
            return False
        self.active.add(jobId)
        heapq.heappush(self.heap, (-priority, jobId))
        return True

    def cancel(self, jobId: int) -> bool:
        if jobId not in self.active:
            return False
        self.active.remove(jobId)
        return True

    def _clean(self) -> None:
        while self.heap and self.heap[0][1] not in self.active:
            heapq.heappop(self.heap)

    def peekJob(self) -> int:
        self._clean()
        if not self.heap:
            return -1
        return self.heap[0][1]

    def popJob(self) -> int:
        self._clean()
        if not self.heap:
            return -1
        _, job_id = heapq.heappop(self.heap)
        self.active.discard(job_id)
        return job_id


# 供 gen / 本地校验用：与 template 相同的行协议
def run_ops(ops):
    outs = []
    obj: Optional[JobQueueSys] = None
    for line in ops:
        line = line.strip()
        if not line:
            continue
        if line.startswith("JobQueueSys("):
            obj = JobQueueSys()
            outs.append("null")
        elif line.startswith("submit("):
            a, b = [int(x.strip()) for x in line[7:-1].split(",")]
            outs.append("true" if obj.submit(a, b) else "false")
        elif line.startswith("cancel("):
            a = int(line[7:-1])
            outs.append("true" if obj.cancel(a) else "false")
        elif line.startswith("popJob("):
            outs.append(str(obj.popJob()))
        elif line.startswith("peekJob("):
            outs.append(str(obj.peekJob()))
        else:
            raise ValueError(line)
    return outs
