from heapq import heappush, heappop


def parse_ver(s):
    # 把 a.b.c 拆成三个整数，按元组比较
    parts = s.split(".")
    return (int(parts[0]), int(parts[1]), int(parts[2]))


def parse_dep(token):
    # 先匹配两位运算符，避免把 >= 拆成 >
    for op in (">=", "<=", ">", "<"):
        pos = token.find(op)
        if pos != -1:
            pid = int(token[:pos])
            ver = parse_ver(token[pos + len(op):])
            return pid, op, ver
    return int(token), None, None


def version_ok(actual, op, bound):
    if op is None:
        return True
    if op == ">=":
        return actual >= bound
    if op == "<=":
        return actual <= bound
    if op == ">":
        return actual > bound
    return actual < bound


def install_order(m, pkgs):
    info = {}
    for pid, ver, deps in pkgs:
        info[pid] = (ver, deps)

    # 先检查全部版本约束，有冲突直接 -1
    for pid, (ver, deps) in info.items():
        for token in deps:
            dep_id, op, bound = parse_dep(token)
            if not version_ok(info[dep_id][0], op, bound):
                return "-1"

    # 边从被依赖者指向依赖者：先安装被依赖者
    g = [[] for _ in range(m)]
    indeg = [0] * m
    for pid, (ver, deps) in info.items():
        for token in deps:
            dep_id, op, bound = parse_dep(token)
            g[dep_id].append(pid)
            indeg[pid] += 1

    # 小根堆保证每次取出当前可安装编号最小的包
    heap = []
    for i in range(m):
        if indeg[i] == 0:
            heappush(heap, i)
    order = []
    while heap:
        u = heappop(heap)
        order.append(u)
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heappush(heap, v)
    # 没能装完说明有环（含自己依赖自己）
    if len(order) != m:
        return "-2"
    return " ".join(str(x) for x in order)


def main():
    m = int(input().strip())
    pkgs = []
    for _ in range(m):
        parts = input().split()
        pid = int(parts[0])
        ver = parse_ver(parts[1])
        deps = parts[2:]
        pkgs.append((pid, ver, deps))
    print(install_order(m, pkgs))


if __name__ == "__main__":
    main()
