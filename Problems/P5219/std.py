# -*- coding: utf-8 -*-


def min_merges(v: list[int]) -> int:
    # 从右向左贪心：维护右侧块的代表值 suf，当前项过大则必须合并
    suf = 10**18
    ans = 0
    for x in reversed(v):
        if x <= suf:
            suf = x
        else:
            ans += 1
            suf += x
    return ans


def main() -> None:
    q = int(input())
    for _ in range(q):
        n = int(input())
        v = list(map(int, input().split()))
        print(min_merges(v))


if __name__ == "__main__":
    main()
