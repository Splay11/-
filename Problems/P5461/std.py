# 连续异或等于前缀异或之差；找最小 q>=p 使 0..q 的前缀异或等于目标值


def xor_pref(n):
    """0 到 n 的连续异或。n<0 时为空区间，返回 0。"""
    if n < 0:
        return 0
    # 连续整数异或每 4 个一循环：n, 1, n+1, 0
    r = n % 4
    if r == 0:
        return n
    if r == 1:
        return 1
    if r == 2:
        return n + 1
    return 0


def min_right(p, w):
    """
    找最小 q>=p，使得 p⊕(p+1)⊕...⊕q = w。
    因为区间异或等于 xor_pref(q) ^ xor_pref(p-1)，
    等价于找最小 q>=p 满足 xor_pref(q) == w ^ xor_pref(p-1)。
    不存在则返回 -1。
    """
    need = w ^ xor_pref(p - 1)
    # 前缀异或只能取到：0、1、模 4 余 0 的数、模 4 余 3 的数
    if need == 0:
        # q=0 或任意 q%4==3
        if p == 0:
            return 0
        return p + (3 - p % 4) % 4
    if need == 1:
        # 任意 q%4==1
        return p + (1 - p % 4) % 4
    if need % 4 == 0:
        # 只能是 q == need
        return need if need >= p else -1
    if need % 4 == 3:
        # 只能是 q == need-1（此时 q%4==2）
        q = need - 1
        return q if q >= p else -1
    return -1


def main():
    # 四级协议：第一行校验字 w，第二行左端点 p
    w = int(input())
    p = int(input())
    print(min_right(p, w))


if __name__ == "__main__":
    main()
