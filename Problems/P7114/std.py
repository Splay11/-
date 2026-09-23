# Bash 博弈：n 能被 k+1 整除则后手胜，否则先手胜


def who_wins(n, k):
    # 每 k+1 颗构成一轮：先手若面对 k+1 的倍数，无论取 1~k 颗，
    # 后手都能取到刚好补成 k+1，把倍数局面丢回给先手
    if n % (k + 1) == 0:
        return "后手"
    return "先手"


def main():
    n, k = map(int, input().split())
    print(who_wins(n, k))


if __name__ == "__main__":
    main()
