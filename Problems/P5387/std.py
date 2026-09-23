# 按 (v+t) 的奇偶分成两类：奇类只能配偶类，偶类之间可以互配


def max_pairs(t, v):
    ev = []
    od = []
    for x in v:
        if (x + t) % 2 == 0:
            ev.append(x)
        else:
            od.append(x)
    pairs = []
    if len(od) > len(ev):
        # 偶类不够，全部拿去配奇类
        for i in range(len(ev)):
            pairs.append((ev[i], od[i]))
    else:
        # 先把奇类配完，剩下的偶类两两互配
        for i in range(len(od)):
            pairs.append((od[i], ev[i]))
        rest = ev[len(od) :]
        for i in range(0, len(rest) - 1, 2):
            pairs.append((rest[i], rest[i + 1]))
    return pairs


def main():
    m, t = map(int, input().split())
    v = list(map(int, input().split()))
    pairs = max_pairs(t, v)
    out = [str(len(pairs))]
    for x, y in pairs:
        out.append(str(x) + " " + str(y))
    print("\n".join(out))


if __name__ == "__main__":
    main()
