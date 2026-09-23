import sys

s = ServiceMgrSys()
print("null")

data = sys.stdin.read().splitlines()
for line in data:
    line = line.strip()
    if not line:
        continue
    if line.startswith("ServiceMgrSys") or line.startswith("ServiceWgSys"):
        continue
    if line.startswith("startService"):
        # startService(1, "serviceA")
        inner = line[line.find("(") + 1 : line.rfind(")")]
        parts = inner.split(",", 1)
        serverId = int(parts[0].strip())
        serviceName = parts[1].strip().strip('"')
        print(str(s.startService(serverId, serviceName)).lower())
    elif line.startswith("addDependency"):
        # addDependency("serviceB", "serviceA")
        inner = line[line.find("(") + 1 : line.rfind(")")]
        parts = inner.split(",", 1)
        fromService = parts[0].strip().strip('"')
        toService = parts[1].strip().strip('"')
        print(str(s.addDependency(fromService, toService)).lower())
    elif line.startswith("isServiceAvailable"):
        # isServiceAvailable("serviceA")
        inner = line[line.find("(") + 1 : line.rfind(")")]
        serviceName = inner.strip().strip('"')
        print(str(s.isServiceAvailable(serviceName)).lower())
    elif line.startswith("rebootServers"):
        # rebootServers([2, 1])
        inner = line[line.find("[") + 1 : line.find("]")]
        ids = [int(x.strip()) for x in inner.split(",") if x.strip()]
        s.rebootServers(ids)
        print("null")
