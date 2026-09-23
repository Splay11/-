import math
import sys


def solve(n, m, p, q, y, a, b):
    """能否使血量 < 1。增幅只乘在魔法二上（与样例一致）；三/四按基础公式结算并消耗增幅。"""
    hp0 = 10**y
    memo = {}

    def dfs(hp, ma, mb, u3, u4, pend):
        if hp < 1:
            return True
        key = (ma, mb, u3, u4, pend)
        prev = memo.get(key)
        if prev is not None and prev <= hp:
            return False
        memo[key] = hp

        # 魔法一：无增幅挂起时，选未用水晶，下一击带倍率
        if pend == 1:
            for i in range(n):
                if (ma >> i) & 1:
                    continue
                if dfs(hp, ma | (1 << i), mb, u3, u4, a[i]):
                    return True

        mult = pend
        # 魔法二
        for j in range(m):
            if (mb >> j) & 1:
                continue
            dmg = b[j] * mult
            if dfs(hp - dmg, ma, mb | (1 << j), u3, u4, 1):
                return True
        # 魔法三：floor(r*p/q)，不乘增幅
        if not u3:
            dmg = hp * p // q
            if dfs(hp - dmg, ma, mb, True, u4, 1):
                return True
        # 魔法四：floor(sqrt(r))，不乘增幅
        if not u4:
            dmg = int(math.isqrt(hp)) if hp >= 0 else 0
            if dfs(hp - dmg, ma, mb, u3, True, 1):
                return True
        return False

    return dfs(hp0, 0, 0, False, False, 1)


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    T = next(it)
    out = []
    for _ in range(T):
        n = next(it)
        m = next(it)
        p = next(it)
        q = next(it)
        y = next(it)
        a = [next(it) for _ in range(n)]
        b = [next(it) for _ in range(m)]
        out.append("Yes" if solve(n, m, p, q, y, a, b) else "No")
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
