MOD = 10 ** 9 + 7


# 计算补全方案数：动态规划，维护最后一段信号字符及其长度的奇偶性
def count_ways(s):
    # odd[c]：最后一段字符为 c，且长度为奇数的方案数
    # even[c]：最后一段字符为 c，且长度为偶数的方案数
    odd = [0, 0]
    even = [0, 0]

    # 初始化第一个字符
    for c in range(2):
        ch = 'A' if c == 0 else 'B'
        if s[0] == '?' or s[0] == ch:
            odd[c] = 1

    # 从第二个字符开始动态规划
    for i in range(1, len(s)):
        new_odd = [0, 0]
        new_even = [0, 0]

        for c in range(2):
            ch = 'A' if c == 0 else 'B'
            if s[i] != '?' and s[i] != ch:
                continue

            # 继续放相同字符：当前段长度奇偶性翻转
            new_odd[c] = (new_odd[c] + even[c]) % MOD
            new_even[c] = (new_even[c] + odd[c]) % MOD

            # 放不同字符：上一段必须是奇数长度才能开启新段
            new_odd[c] = (new_odd[c] + odd[c ^ 1]) % MOD

        odd, even = new_odd, new_even

    # 最后一段必须是奇数长度
    return (odd[0] + odd[1]) % MOD


def main():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        s = input().strip()
        ans.append(str(count_ways(s)))

    print("\n".join(ans))


if __name__ == "__main__":
    main()
