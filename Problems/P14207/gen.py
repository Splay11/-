# -*- coding: utf-8 -*-
"""
按 codefun2000-problem-generator 第 8 节：
- 8.1：造数 + 求标 + 写盘；混合随机/构造；覆盖六类测试思想。
- 8.2：10 组，data/ 下 1.in…10.in 连续编号。
- 8.3：前 8 组中小规模；后 2 组近题面 n 上界（29）的大数据。
- 8.4：显式 hack 组，见 data/README.md。
- 8.5：.in 最后一行数据后无换行符；.out 末尾有且仅有一个 \\n。
- 8.6：生成后对每组用基准 std（std.py）+ template 重算比对。
"""

import ast
import importlib.util
import json
import random
import subprocess
import sys
from pathlib import Path

SEED = 142070001
RNG = random.Random(SEED)

DIR = Path(__file__).resolve().parent
DATA = DIR / "data"


def load_solution():
    spec = importlib.util.spec_from_file_location("stdmod", DIR / "std.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Solution()


SOL = load_solution()


def expected(n: int, guards):
    g2 = [[int(p[0]), int(p[1])] for p in guards]
    return SOL.countShortestPaths(n, g2)


def fmt_input(n: int, guards) -> str:
    """与题面样例同形：n,[(x,y),...] 或 n,[]，紧凑无多余空格。"""
    if not guards:
        return f"{n},[]"
    inner = ",".join(f"({int(p[0])},{int(p[1])})" for p in guards)
    return f"{n},[{inner}]"


def write_in(path: Path, content: str):
    """8.5：输入文件末尾不要换行符（无 EOF 换行）。"""
    if content.endswith("\n"):
        content = content.rstrip("\n")
    path.write_bytes(content.encode("utf-8"))


def write_out(path: Path, out_list):
    """8.5：输出文件末尾有且仅有一个换行符。"""
    line = json.dumps(out_list, separators=(",", ":"), ensure_ascii=False) + "\n"
    path.write_bytes(line.encode("utf-8"))


def write_case(idx: int, n: int, guards):
    DATA.mkdir(parents=True, exist_ok=True)
    s = fmt_input(n, guards)
    out = expected(n, guards)
    write_in(DATA / f"{idx}.in", s)
    write_out(DATA / f"{idx}.out", out)


def run_std_py_on_in_bytes(raw: bytes) -> str:
    """用 std.py + template 跑 stdin（字节级，与 .in 文件一致）。"""
    std = (DIR / "std.py").read_text(encoding="utf-8")
    tpl = (DIR / "template.py").read_text(encoding="utf-8")
    script = std + "\n" + tpl
    p = subprocess.run(
        [sys.executable, "-c", script],
        input=raw,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(DIR),
    )
    if p.returncode != 0:
        raise RuntimeError(p.stderr.decode("utf-8", errors="replace"))
    return p.stdout.decode("utf-8").replace("\r\n", "\n")


def verify_all():
    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_bytes()
        exp = (DATA / f"{i}.out").read_text(encoding="utf-8")
        got = run_std_py_on_in_bytes(raw)
        if got != exp:
            raise SystemExit(f"case {i} mismatch:\nexp={exp!r}\ngot={got!r}")


def gen_random_guards(n: int, m: int, rng: random.Random):
    return [[rng.randrange(n), rng.randrange(n)] for _ in range(m)]


def build_cases():
    """
    返回 (n, guards) 列表，长度 10。
    1-3 样例；4-8 中小；9-10 近满 n=29。
    """
    r7 = random.Random(SEED + 7)
    r10 = random.Random(SEED + 10)
    cases = [
        # 1-3 样例（8.1 样例类）
        (3, [[1, 1]]),
        (5, [[2, 1]]),
        (5, [[2, 2]]),
        # 4 基础：无哨兵最短路
        (3, []),
        # 5 边界：堵入口格
        (5, [[0, 2]]),
        # 6 边界：较大奇数 n、中心九宫格（与样例 3 同形不同规模）
        (7, [[3, 3]]),
        # 7 随机：中小 n
        (11, gen_random_guards(11, 10, r7)),
        # 8 构造：链状/绕路压力（中等 n）
        (15, [[7, 7], [6, 7], [8, 7], [7, 6], [7, 8]]),
        # 9-10 大数据：n=29（题面上界）
        (29, []),
        (29, gen_random_guards(29, 200, r10)),
    ]
    assert len(cases) == 10
    return cases


def main():
    for i, (n, g) in enumerate(build_cases(), start=1):
        write_case(i, n, g)
    verify_all()


if __name__ == "__main__":
    main()
