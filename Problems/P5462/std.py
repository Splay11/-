LIM = 10**16


def make_min_number(length, digit_sum):
    # 构造长度为 length、数位和为 digit_sum 的最小十进制数
    first = max(1, digit_sum - 9 * (length - 1))
    if first > 9 or first > digit_sum:
        return None
    rest = digit_sum - first
    digits = [0] * length
    digits[0] = first
    # 余数尽量放到右边，左边才能尽量小
    for i in range(length - 1, 0, -1):
        take = min(9, rest)
        digits[i] = take
        rest -= take
    if rest != 0:
        return None
    value = 0
    for d in digits:
        value = value * 10 + d
    return value


def min_code(w):
    # 从小到大枚举位数 L，第一个合法编号就是最小的
    for length in range(1, 18):
        if w % length != 0:
            continue
        digit_sum = w // length
        if digit_sum < 1 or digit_sum > 9 * length:
            continue
        if length == 17:
            # 闭区间上界 10^16 是唯一的 17 位数
            if digit_sum == 1:
                return LIM
            continue
        value = make_min_number(length, digit_sum)
        if value is None or value > LIM:
            continue
        return value
    return -1


def solve_all(ws):
    return [min_code(w) for w in ws]


def main():
    q = int(input())
    ws = list(map(int, input().split()))
    ans = solve_all(ws)
    print(" ".join(str(x) for x in ans))


if __name__ == "__main__":
    main()
