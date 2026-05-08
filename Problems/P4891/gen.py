from __future__ import annotations

from pathlib import Path
import random


def solve_interval_scheduling(n: int, intervals: list[tuple[int, int]]) -> int:
    """与 std 一致：端点包含，不重叠当且仅当后一段起点严格大于上一段终点。"""
    intervals_sorted = sorted(intervals, key=lambda x: (x[1], x[0]))
    last_end = -(10**30)
    cnt = 0
    for s, e in intervals_sorted:
        if s > last_end:
            cnt += 1
            last_end = e
    return cnt


def write_case(data_dir: Path, idx: int, n: int, flat: list[int]) -> None:
    lines = [str(n), " ".join(str(x) for x in flat)]
    body = "\n".join(lines)
    ans = str(solve_interval_scheduling(n, [(flat[2 * i], flat[2 * i + 1]) for i in range(n)]))
    # 强制 LF，避免 Windows 默认 CRLF 与评测机不一致。
    with (data_dir / f"{idx}.in").open("w", encoding="utf-8", newline="\n") as f:
        f.write(body)
    with (data_dir / f"{idx}.out").open("w", encoding="utf-8", newline="\n") as f:
        f.write(ans + "\n")


def main() -> None:
    rng = random.Random(4891)
    data_dir = Path(__file__).resolve().parent / "data"
    data_dir.mkdir(exist_ok=True)

    cases: list[tuple[int, list[int], str]] = []

    # 1 样例
    cases.append((4, [4, 9, 9, 11, 13, 19, 10, 17], "样例：与题面一致，验证输入格式与端点包含规则。"))

    # 2 边界：单区间
    cases.append((1, [0, 10**9], "边界：$n=1$，答案为 $1$。"))

    # 3 构造：两两不重叠，答案为 $n$
    n3 = 6
    flat3 = []
    t = 0
    for _ in range(n3):
        flat3.extend([t, t + 1])
        t += 2
    cases.append((n3, flat3, "构造：链式无交区间，贪心应取满。"))

    # 4 构造：全部相同，答案为 $1$
    cases.append((7, [1, 5] * 7, "构造：完全相同区间，卡重复计数与去重误用。"))

    # 5 hack：按开始时间或区间长度贪心会失败
    cases.append((3, [1, 10, 2, 3, 4, 5], "hack：大区间挡在前面，正解按结束时间取两个小区间。"))

    # 6 hack：嵌套区间，按结束时间仍能取多个不相交小区间
    cases.append(
        (
            5,
            [1, 100, 2, 10, 11, 20, 21, 30, 31, 40],
            "hack：长区间包裹多段短区间，检验排序关键字是否为结束时间。",
        )
    )

    # 7 边界：相邻端点相接，应视为冲突
    cases.append((3, [0, 1, 1, 2, 2, 3], "边界：相邻区间在公共端点处重叠，最多取 $1$。"))

    # 8 随机小数据
    n8 = 30
    flat8 = []
    for _ in range(n8):
        s = rng.randint(0, 50)
        e = rng.randint(s, 80)
        flat8.extend([s, e])
    cases.append((n8, flat8, "随机：小规模混合分布，便于与暴力对拍。"))

    # 9 大数据：随机大规模
    n9 = 200_000
    flat9 = []
    for _ in range(n9):
        s = rng.randint(0, 10**9)
        e = rng.randint(s, min(10**9, s + rng.randint(0, 10**6)))
        flat9.extend([s, e])
    cases.append((n9, flat9, "大数据：$n=2\\times 10^5$，时间坐标到 $10^9$，压测排序与扫描。"))

    # 10 大数据：相同右端点、随机左端点（排序稳定与 long long）
    n10 = 200_000
    R = 10**12
    flat10 = []
    for i in range(n10):
        s = rng.randint(0, R - 1)
        flat10.extend([s, R])
    cases.append((n10, flat10, "大数据：共用极大右端点，卡排序与整型范围。"))

    for idx, (n, flat, desc) in enumerate(cases, 1):
        if len(flat) != 2 * n:
            raise ValueError(f"case {idx}: flat size mismatch")
        write_case(data_dir, idx, n, flat)

    readme_lines = [
        "# 数据生成说明",
        "",
        "题面未给出显式数值上界；本地包采用：",
        "",
        "- 小数据组（$1$–$8$）：$n$ 不超过几十，时间坐标在较小范围内。",
        "- 大数据组（$9$–$10$）：$n=2\\times 10^5$，时间坐标至 $10^{12}$ 量级。",
        "",
        "| 组别 | 类型 | 说明 |",
        "|---:|---|---|",
    ]
    for idx, (_, _, desc) in enumerate(cases, 1):
        kind = "大数据" if idx >= 9 else "小数据"
        readme_lines.append(f"| {idx} | {kind} | {desc} |")
    readme_lines.extend(
        [
            "",
            "主要针对的错误解法：",
            "",
            "- 按开始时间或区间长度贪心。",
            "- 把「端点相接」当成不冲突（应用 `>` 而不是 `>=` 判断衔接）。",
            "- 排序关键字错误（按左端点或区间长度）。",
            "- 坐标与累加使用 32 位整型溢出。",
        ]
    )
    with (data_dir / "README.md").open("w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(readme_lines) + "\n")

    for idx in range(1, 11):
        raw = (data_dir / f"{idx}.in").read_text(encoding="utf-8")
        lines = raw.splitlines()
        n = int(lines[0].strip())
        parts = lines[1].split()
        nums = list(map(int, parts))
        expected = str(solve_interval_scheduling(n, [(nums[2 * i], nums[2 * i + 1]) for i in range(n)])) + "\n"
        actual = (data_dir / f"{idx}.out").read_text(encoding="utf-8")
        if actual != expected:
            raise RuntimeError(f"case {idx} output mismatch:\nexpected={expected!r}\nactual={actual!r}")


if __name__ == "__main__":
    main()
