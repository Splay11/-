# -*- coding: utf-8 -*-
"""相邻不同串计数 — DP 逐位递推
状态：f[pat_idx][char] = 前缀[0..pat_idx]中以 char 结尾的合法方案数
转移：f[i][c] = total[i-1] - f[i-1][c]（即上一位的总数减去上一位以当前字符c结尾的数）
复杂度：O(26 * Σm)
"""
import sys

MOD = 10 ** 9 + 7


def solve_one(m: int, pat: str) -> int:
    # f[c]: 当前前缀以字符 c 结尾的方案数，下标 0-25 对应 'a'-'z'
    f = [0] * 26

    # 第一位初始化
    if pat[0] == '?':
        for c in range(26):
            f[c] = 1
    else:
        f[ord(pat[0]) - 97] = 1

    total = sum(f) % MOD

    for i in range(1, m):
        ch = pat[i]
        nf = [0] * 26  # 下一位的 dp
        if ch == '?':
            # 当前位为 ?，每一位都可以取，只要不等于前一位
            for c in range(26):
                nf[c] = (total - f[c]) % MOD
        else:
            # 固定字符，只有该字符可取值
            c = ord(ch) - 97
            nf[c] = (total - f[c]) % MOD

        f = nf
        total = sum(f) % MOD
        if total == 0:
            break  # 无法继续，提前退出

    return total


def main() -> None:
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    T = int(next(it))
    out_lines = []
    for _ in range(T):
        m = int(next(it))
        pat = next(it).decode()
        out_lines.append(str(solve_one(m, pat)))
    sys.stdout.write("\n".join(out_lines))


if __name__ == "__main__":
    main()
