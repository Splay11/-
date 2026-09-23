def parse(expression):
    """连续数字合成一个 0..99 的整数，运算符单独记下。
    不能按单个字符拆，否则 12 会被拆成 1 和 2。
    """
    nums = []
    ops = []
    i = 0
    n = len(expression)
    while i < n:
        ch = expression[i]
        if ch == "+" or ch == "-" or ch == "*":
            ops.append(ch)
            i += 1
        else:
            val = 0
            while i < n and expression[i].isdigit():
                val = val * 10 + ord(expression[i]) - 48
                i += 1
            nums.append(val)
    return nums, ops


def combine(a, op, b):
    """按运算符把左右两个子表达式的值合在一起。"""
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    return a * b


def dfs(left, right, nums, ops, memo):
    """计算 nums[left..right] 这一段所有加括号方式的结果。
    枚举最后一次运算发生在第 k 个运算符上，左右各自递归。
    """
    key = (left, right)
    if key in memo:
        return memo[key]
    if left == right:
        memo[key] = [nums[left]]
        return memo[key]
    res = []
    k = left
    while k < right:
        left_vals = dfs(left, k, nums, ops, memo)
        right_vals = dfs(k + 1, right, nums, ops, memo)
        op = ops[k]
        for x in left_vals:
            for y in right_vals:
                res.append(combine(x, op, y))
        k += 1
    memo[key] = res
    return res


def solve(expression):
    """返回所有加括号结果，相同结果按不同划分各保留一次，再从小到大排序。"""
    nums, ops = parse(expression)
    vals = dfs(0, len(nums) - 1, nums, ops, {})
    vals.sort()
    return vals


def main():
    # 一行表达式；先输出方案数，再输出排序后的全部结果
    expression = input().strip()
    vals = solve(expression)
    print(len(vals))
    print(" ".join(str(x) for x in vals))


if __name__ == "__main__":
    main()
