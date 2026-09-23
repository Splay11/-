"""
P5222 等级序列还原 - 数据生成器
生成 10 组测试数据到 data/ 目录
"""
import os
import random

random.seed(20250808)

DATA_DIR = "data"


def solve_one(n, k, S, R):
    """解题函数，与 std.py 一致"""
    for M in range(1, 7):
        if not (n - k <= R <= (n - k) * M):
            continue
        if not (k * M <= S - R <= k * 6):
            continue

        retained = []
        extra = R - (n - k)
        for _ in range(n - k):
            add = extra if extra <= M - 1 else M - 1
            retained.append(1 + add)
            extra -= add

        removed = []
        extra = (S - R) - k * M
        for _ in range(k):
            add = extra if extra <= 6 - M else 6 - M
            removed.append(M + add)
            extra -= add

        return retained + removed
    return None


def format_output(ans):
    if ans is None:
        return "-1"
    return " ".join(map(str, ans))


def gen_solvable(n, k):
    """生成一个可解的四元组"""
    M = random.randint(1, 6)
    rem = n - k
    vals = [random.randint(1, M) for _ in range(rem)]
    R = sum(vals)
    removed_vals = [random.randint(M, 6) for _ in range(k)]
    S = R + sum(removed_vals)
    return n, k, S, R


def gen_unsolvable():
    """生成一个无解的四元组"""
    n = random.randint(2, 10)
    k = random.randint(1, n - 1)
    reason = random.randint(1, 3)

    if reason == 1:
        # R < n-k（保留和太小）
        R = max(0, (n - k) - random.randint(1, n - k))
        S = max(R + 1, R + random.randint(k, k * 6))
    elif reason == 2:
        # S-R > k*6（召回和太大）
        R = random.randint(n - k, (n - k) * 6)
        S = R + k * 6 + random.randint(1, 10)
    else:
        # 交叉不可行：M=low 时召回不够，M=high 时保留超限
        M_low = random.randint(1, 4)
        rem = n - k
        R = (M_low + 1) * rem + random.randint(1, 5)
        diff = M_low * k - random.randint(1, k)
        S = R + max(1, diff)

    return n, k, S, R


def write_data(idx, n, k, S, R):
    in_path = os.path.join(DATA_DIR, f"{idx}.in")
    out_path = os.path.join(DATA_DIR, f"{idx}.out")
    with open(in_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"{n} {k} {S} {R}")
    ans = solve_one(n, k, S, R)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(format_output(ans) + "\n")


def verify(idx):
    in_path = os.path.join(DATA_DIR, f"{idx}.in")
    out_path = os.path.join(DATA_DIR, f"{idx}.out")
    with open(in_path, "r") as f:
        n, k, S, R = map(int, f.read().strip().split())
    expected = solve_one(n, k, S, R)
    with open(out_path, "r") as f:
        actual = f.read().strip()
    if expected is None:
        return actual == "-1"
    if actual == "-1":
        return False
    vals = list(map(int, actual.split()))
    if len(vals) != n or any(v < 1 or v > 6 for v in vals) or sum(vals) != S:
        return False
    sv = sorted(vals)
    return sum(sv[:n - k]) == R


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    # 10 组测试数据
    cases = [
        # 1. 题面样例 — 有解
        (4, 2, 15, 5),
        # 2. 题面样例 — 有解
        (3, 1, 10, 6),
        # 3. 题面样例 — 无解
        (3, 1, 10, 2),
        # 4. 小数据 — 有解
        gen_solvable(5, 2),
        # 5. 小数据 — 有解 (M=1边界)
        (3, 1, 3, 2),
        # 6. 无解
        gen_unsolvable(),
        # 7. 中等数据 — 有解
        gen_solvable(50, 20),
        # 8. 中等数据 — 无解
        gen_unsolvable(),
        # 9. 大数据 — 有解
        gen_solvable(200000, 50000),
        # 10. 大数据 — 有解
        gen_solvable(198000, 100000),
    ]

    print("生成数据...")
    for i, case in enumerate(cases, 1):
        n, k, S, R = case
        write_data(i, n, k, S, R)
        print(f"  第{i:2d}组: n={n}, k={k}, S={S}, R={R}")

    print("\n自校验...")
    for i in range(1, 11):
        ok = verify(i)
        status = "PASS" if ok else "FAIL"
        print(f"  第{i:2d}组: {status}")
        if not ok:
            print("  校验失败！")
            import sys; sys.exit(1)

    print("\nAll 10 groups PASS!")


if __name__ == "__main__":
    main()
