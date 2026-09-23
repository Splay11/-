# 等和连续段最多划分：候选段和取自前缀和，验证倍数前缀均出现

def can_split(pref_set, T, k):
    # 需要前缀和中出现 T, 2T, ..., kT
    for i in range(1, k + 1):
        if (T * i) not in pref_set:
            return False
    return True


def main():
    n = int(input())
    a = list(map(int, input().split()))
    S = sum(a)

    if S == 0:
        # 每段和为 0：前缀和每次回到 0 就结束一段
        p = 0
        cnt = 0
        for x in a:
            p += x
            if p == 0:
                cnt += 1
        print(cnt)
        return

    pref = 0
    pref_set = set()
    for x in a:
        pref += x
        pref_set.add(pref)

    best = 1
    pref = 0
    # 枚举第一段结束位置对应的段和 T
    for i in range(n - 1):
        pref += a[i]
        T = pref
        if T == 0:
            continue
        if S % T != 0:
            continue
        k = S // T
        if k <= best:
            continue
        if can_split(pref_set, T, k):
            best = k
    print(best)


if __name__ == "__main__":
    main()
