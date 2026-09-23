# 异或前缀 + 哈希：统计有多少前缀异或 pref^k 曾出现

from collections import defaultdict


def main():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    cnt = defaultdict(int)
    cnt[0] = 1  # 空前缀异或为 0
    pref = 0
    ans = 0
    for x in a:
        pref ^= x
        # 需要 pref ^ pre = k，即 pre = pref ^ k
        ans += cnt[pref ^ k]
        cnt[pref] += 1
    print(ans)


if __name__ == "__main__":
    main()
