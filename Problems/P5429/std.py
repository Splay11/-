# 按编号升序回溯，枚举长度为 t 的无冲突组合，统计全部合法方案并保留字典序前 3 份


def collect_schemes(m, t, g, lo, hi, w):
    """
    在 1..m 中取 t 个模块。相邻编号差必须大于 g，负荷和落在 [lo, hi]。
    回溯按编号递增展开，因此得到的方案本身就是字典序。
    返回 (总份数, 前 3 份方案)。
    """
    count = 0
    top = []

    def dfs(start, chosen, total):
        nonlocal count
        # 已经取满 t 个：只检查负荷和
        if len(chosen) == t:
            if lo <= total <= hi:
                count += 1
                if len(top) < 3:
                    top.append(chosen[:])
            return
        remain = t - len(chosen)
        # 从 start 起枚举下一个编号；编号必须递增，保证字典序
        for i in range(start, m + 1):
            # 剩下位置不够凑满 t 个，后面更大的 i 更不够
            if m - i + 1 < remain:
                break
            chosen.append(i)
            # 下一个合法起点至少是 i+g+1，这样相邻差一定大于 g
            dfs(i + g + 1, chosen, total + w[i - 1])
            chosen.pop()

    dfs(1, [], 0)
    return count, top


def main():
    m, t, g, lo, hi = map(int, input().split())
    w = list(map(int, input().split()))
    count, top = collect_schemes(m, t, g, lo, hi, w)
    print(count)
    for scheme in top:
        print(" ".join(str(x) for x in scheme))


if __name__ == "__main__":
    main()
