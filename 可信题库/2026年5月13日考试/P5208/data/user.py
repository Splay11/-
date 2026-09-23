from typing import List


class GCSystem:
    def __init__(self, youngSize: int):
        pass

    def createObject(self, objectId: int) -> None:
        pass

    def markObjects(self, objectIds: List[int]) -> None:
        pass

    def manualGC(self, generation: int) -> None:
        pass

    def getLiveObjects(self, generation: int) -> List[int]:
        return []
