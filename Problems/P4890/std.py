def solve(n: int) -> int:
    # 正整数 N 的最高二进制位下标就是答案。
    return n.bit_length() - 1


n = int(input())
print(solve(n))
