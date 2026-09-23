from typing import List


class ServiceMgrSys:
    def __init__(self):
        pass

    def rebootServers(self, serverIds: List[int]) -> None:
        pass

    def startService(self, serverId: int, serviceName: str) -> bool:
        return False

    def addDependency(self, fromServiceName: str, toServiceName: str) -> bool:
        return False

    def isServiceAvailable(self, serviceName: str) -> bool:
        return False
