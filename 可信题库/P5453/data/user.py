class ParkingLane:
    def __init__(self, capacity: int):
        pass

    def arrive(self, carId: int) -> bool:
        return False

    def admit(self) -> bool:
        return False

    def depart(self, carId: int) -> int:
        return -1

    def undo(self) -> bool:
        return False

    def front(self) -> int:
        return -1

    def waiting(self) -> int:
        return 0

    def size(self) -> int:
        return 0
