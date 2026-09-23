class JobQueueSys:
    def __init__(self):
        pass

    def submit(self, jobId: int, priority: int) -> bool:
        return False

    def cancel(self, jobId: int) -> bool:
        return False

    def popJob(self) -> int:
        return -1

    def peekJob(self) -> int:
        return -1
