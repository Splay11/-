# 基站总干扰指数：用单调栈求左右最近严格更大元素，距离超过 k 则该侧贡献为 0。


MOD = 10**9 + 7


def total_interference(power, k):
    n = len(power)

    # nge_left[i]：i 左侧最近且严格更大的下标；没有则为 -1
    nge_left = [-1] * n
    stack = []
    for i in range(n):
        # 栈里只保留比当前值更大的候选，栈顶就是最近的那个
        while stack and power[stack[-1]] <= power[i]:
            stack.pop()
        if stack:
            nge_left[i] = stack[-1]
        stack.append(i)

    # nge_right[i]：i 右侧最近且严格更大的下标；没有则为 -1
    nge_right = [-1] * n
    stack = []
    for i in range(n):
        # 当前值能作为栈中更小元素的「右侧第一个更大」
        while stack and power[stack[-1]] < power[i]:
            nge_right[stack.pop()] = i
        stack.append(i)

    ans = 0
    for i in range(n):
        left = nge_left[i]
        # 最近更大元素必须落在长度为 k 的搜索窗口内，否则贡献为 0
        if left != -1 and i - left <= k:
            ans = (ans + power[i] * (i - left)) % MOD
        right = nge_right[i]
        if right != -1 and right - i <= k:
            ans = (ans + power[i] * (right - i)) % MOD
    return ans


def main():
    # 第一行：全部基站强度，n 由元素个数得到
    power = list(map(int, input().split()))
    # 第二行：最多向一侧搜索的基站个数
    k = int(input())
    print(total_interference(power, k))


if __name__ == "__main__":
    main()
