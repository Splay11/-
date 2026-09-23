import sys


def solve_case(k, s, zones):
    # 按禁入区间左端点排序
    zones.sort()

    cur_l, cur_r = zones[0]

    for i in range(1, k):
        L, R = zones[i]

        if L <= cur_r + 1:
            if R > cur_r:
                cur_r = R
        else:
            if cur_l <= s <= cur_r:
                return min(s - cur_l + 1, cur_r - s + 1)
            cur_l, cur_r = L, R

    if cur_l <= s <= cur_r:
        return min(s - cur_l + 1, cur_r - s + 1)

    return 0


def main():
    input = sys.stdin.readline
    t = int(input().strip())
    ans = []

    for _ in range(t):
        k, s = map(int, input().split())
        zones = []
        for _ in range(k):
            L, R = map(int, input().split())
            zones.append((L, R))
        ans.append(str(solve_case(k, s, zones)))

    print("\n".join(ans))


if __name__ == "__main__":
    main()
