class FileLockBoard:
    def __init__(self):
        self.own = {}

    def lock(self, fileId: int, ownerId: int) -> bool:
        if fileId in self.own:
            return False
        self.own[fileId] = ownerId
        return True

    def unlock(self, fileId: int, ownerId: int) -> bool:
        if self.own.get(fileId) != ownerId:
            return False
        del self.own[fileId]
        return True

    def holder(self, fileId: int) -> int:
        return self.own.get(fileId, -1)

    def lockedCount(self) -> int:
        return len(self.own)
