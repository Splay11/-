from typing import List, Dict, Set


class ServiceMgrSys:
    def __init__(self):
        # serviceName -> 正在运行该服务的服务器集合
        self.running: Dict[str, Set[int]] = {}
        # serverId -> 该服务器上正在运行的服务集合
        self.on_server: Dict[int, Set[str]] = {}
        # fromService -> 其直接依赖的服务集合
        self.deps: Dict[str, Set[str]] = {}

    def rebootServers(self, serverIds: List[int]) -> None:
        for sid in serverIds:
            for name in list(self.on_server.get(sid, set())):
                self.running[name].discard(sid)
                if not self.running[name]:
                    del self.running[name]
            self.on_server[sid] = set()

    def startService(self, serverId: int, serviceName: str) -> bool:
        if serviceName in self.on_server.get(serverId, set()):
            return False
        self.on_server.setdefault(serverId, set()).add(serviceName)
        self.running.setdefault(serviceName, set()).add(serverId)
        return True

    def addDependency(self, fromServiceName: str, toServiceName: str) -> bool:
        if toServiceName in self.deps.get(fromServiceName, set()):
            return False
        self.deps.setdefault(fromServiceName, set()).add(toServiceName)
        return True

    def isServiceAvailable(self, serviceName: str) -> bool:
        memo: Dict[str, bool] = {}

        def dfs(name: str) -> bool:
            if name in memo:
                return memo[name]
            # 自身至少一个实例在运行
            if name not in self.running or not self.running[name]:
                memo[name] = False
                return False
            # 所有直接依赖都必须可提供服务（递归，覆盖传递依赖）
            for dep in self.deps.get(name, set()):
                if not dfs(dep):
                    memo[name] = False
                    return False
            memo[name] = True
            return True

        return dfs(serviceName)
