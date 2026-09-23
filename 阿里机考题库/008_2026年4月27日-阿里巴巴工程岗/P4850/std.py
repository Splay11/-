def odd_palindrome_radius(labels):
    # 在化简后的品类序列上求最长奇回文半径
    n = len(labels)
    radius = [0] * n
    left, right = 0, -1
    best = 0

    for i in range(n):
        if i > right:
            k = 1
        else:
            k = min(radius[left + right - i], right - i + 1)

        while i - k >= 0 and i + k < n and labels[i - k] == labels[i + k]:
            k += 1

        radius[i] = k
        best = max(best, k)

        if i + k - 1 > right:
            left = i - k + 1
            right = i + k - 1

    return best


def max_clearances(n, categories):
    stack = []

    # 模拟不补货箱时的全部配对清除
    for cat in categories:
        if stack and stack[-1] == cat:
            stack.pop()
        else:
            stack.append(cat)

    reduced_len = len(stack)
    base = (n - reduced_len) // 2

    # 已全部清完，补入单个货箱无法产生新清除
    if reduced_len == 0:
        return base

    extra = odd_palindrome_radius(stack)
    return base + extra


def main():
    t = int(input())
    out_lines = []
    for _ in range(t):
        n = int(input())
        categories = list(map(int, input().split()))
        out_lines.append(str(max_clearances(n, categories)))
    print("\n".join(out_lines))


if __name__ == "__main__":
    main()
