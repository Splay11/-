class FileLockBoard:
    def __init__(self):
        pass

    def lock(self, fileId: int, ownerId: int) -> bool:
        return False

    def unlock(self, fileId: int, ownerId: int) -> bool:
        return False

    def holder(self, fileId: int) -> int:
        return -1

    def lockedCount(self) -> int:
        return 0
