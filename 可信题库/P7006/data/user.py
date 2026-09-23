class ClusterPool:
    def __init__(self):
        pass

    def addNode(self, nodeId: int, capacity: int) -> bool:
        return False

    def removeNode(self, nodeId: int) -> bool:
        return False

    def submit(self, jobId: int, size: int) -> int:
        return -1

    def kill(self, jobId: int) -> bool:
        return False

    def usedOf(self, nodeId: int) -> int:
        return -1

    def freeOf(self, nodeId: int) -> int:
        return -1

    def jobNode(self, jobId: int) -> int:
        return -1
