def solve(cards, k):
    """从两端一共拿 k 张，等价于中间留下连续的 n-k 张。
    要使拿走的点数最大，就要让留下的这一段点数之和最小。
    用定长滑动窗口扫一遍留下段即可。
    """
    n = len(cards)
    total = 0
    for x in cards:
        total += x
    leave = n - k
    # 必须拿完全部牌时，中间不留牌
    if leave == 0:
        return total
    window = 0
    for i in range(leave):
        window += cards[i]
    best = window
    for i in range(leave, n):
        window += cards[i] - cards[i - leave]
        if window < best:
            best = window
    return total - best


def main():
    # 第一行 n、k，第二行 n 张牌的点数
    n, k = map(int, input().split())
    cards = list(map(int, input().split()))
    print(solve(cards, k))


if __name__ == "__main__":
    main()
