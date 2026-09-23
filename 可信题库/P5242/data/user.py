class ParkingLot:
    def __init__(self, n: int):
        pass

    def reserve(self, carId: int, start: int, end: int) -> int:
        return -1

    def cancel(self, carId: int) -> bool:
        return False

    def spotOf(self, carId: int) -> int:
        return -1

    def busyCount(self, time: int) -> int:
        return 0
