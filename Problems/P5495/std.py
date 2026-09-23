def can_give(candies, k, each):
    # 每人 each 颗时，每堆能切出 candies_i / each 份；份数够 k 个小孩即可
    if each == 0:
        return True
    got = 0
    for c in candies:
        got += c // each
        if got >= k:
            return True
    return False


def max_candies(candies, k):
    # 答案越大越难满足，在 [0, max(candies)] 上二分最大可行值
    left = 0
    right = candies[0]
    for c in candies:
        if c > right:
            right = c
    while left < right:
        mid = (left + right + 1) // 2
        if can_give(candies, k, mid):
            left = mid
        else:
            right = mid - 1
    return left


def main():
    # 第一行 n 与小孩数 k，第二行 n 堆糖果
    parts = list(map(int, input().split()))
    n = parts[0]
    k = parts[1]
    candies = list(map(int, input().split()))
    print(max_candies(candies[:n], k))


if __name__ == "__main__":
    main()
