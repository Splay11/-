class MicQueue:
    def __init__(self):
        pass

    def enroll(self, songId: int, heat: int) -> bool:
        return False

    def nextPlay(self) -> int:
        return -1

    def boost(self, songId: int, addHeat: int) -> bool:
        return False

    def cancel(self, songId: int) -> bool:
        return False

    def waiting(self) -> int:
        return 0
