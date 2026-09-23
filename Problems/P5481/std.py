# 枚举第二种操作次数；全体先按满击中算点名，再把豁免分到代价最小的位置


def cost_with_type2(load, heavy, light, type2):
    """第二种操作恰好 type2 次时的最少总次数。"""
    t0_sum = 0
    t0 = []
    slack = []
    for x in load:
        # 先假设每个数都被第二种操作打中 type2 次
        rest = x - light * type2
        if rest > 0:
            need = (rest + heavy - 1) // heavy
            t0_sum += need
            t0.append(need)
            slack.append(0)
        else:
            t0.append(0)
            if x <= 0:
                slack.append(type2)
            else:
                need_b = (x + light - 1) // light
                slack.append(max(0, type2 - need_b))
    # 第二种操作必须选中某几个下标共 type2 次，这些下标当次不会被减 B
    free = sum(slack)
    if free >= type2:
        return type2 + t0_sum
    extra = type2 - free
    best_delta = None
    for i, x in enumerate(load):
        used = slack[i] + extra
        if used > type2:
            continue
        hits = type2 - used
        rest = x - light * hits
        need = 0 if rest <= 0 else (rest + heavy - 1) // heavy
        delta = need - t0[i]
        if best_delta is None or delta < best_delta:
            best_delta = delta
    if best_delta is None:
        return 10**18
    return type2 + t0_sum + best_delta


def min_ops(load, heavy, light):
    """最少操作次数。n=1 时第二种操作无效。"""
    only_a = 0
    for x in load:
        if x > 0:
            only_a += (x + heavy - 1) // heavy
    n = len(load)
    if n == 1:
        return only_a
    need_b = []
    for x in load:
        if x > 0:
            need_b.append((x + light - 1) // light)
        else:
            need_b.append(0)
    max_need = max(need_b)
    sum_need = sum(need_b)
    # 纯第二种操作也够：每个数要 ceil(a_i/B) 次击中，总击中为 S*(n-1)
    max_s = max(max_need, (sum_need + n - 2) // (n - 1))
    best = only_a
    # S 再大也比只减 A 更亏
    if max_s > only_a:
        max_s = only_a
    for type2 in range(0, max_s + 1):
        cur = cost_with_type2(load, heavy, light, type2)
        if cur < best:
            best = cur
    return best


def main():
    n = int(input())
    heavy, light = map(int, input().split())
    load = list(map(int, input().split()))
    print(min_ops(load, heavy, light))


if __name__ == "__main__":
    main()
