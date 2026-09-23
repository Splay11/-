def solve(plans, logs):
    # plans: list of (rid, scene, ver) in order
    # logs: list of (rid, ver, platform, status)
    ready = set()
    for rid, ver, plat, status in logs:
        if status == "READY":
            ready.add((rid, ver, plat))
    missing = []
    for rid, scene, ver in plans:
        ok = True
        for plat in ("android", "ios", "pc"):
            if (rid, ver, plat) not in ready:
                ok = False
                break
        if not ok:
            missing.append(rid)
    return missing if missing else ["none"]


if __name__ == "__main__":
    R, C = map(int, input().split())
    plans = []
    for _ in range(R):
        rid, scene, ver = input().split()
        plans.append((rid, scene, ver))
    logs = []
    for _ in range(C):
        rid, ver, plat, status = input().split()
        logs.append((rid, ver, plat, status))
    for line in solve(plans, logs):
        print(line)
