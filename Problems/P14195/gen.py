# -*- coding: utf-8 -*-
"""
按 codefun2000-problem-generator 第 8 节 + LeetCode 模式：
- 10 组数据；.in 与题面样例同形；.in 末尾无换行；.out 末尾单换行；
- 生成后 std.py+template.py 逐组重算校验。
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
DATA = DIR / "data"


def load_solution():
    spec = importlib.util.spec_from_file_location("stdmod", DIR / "std.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Solution()


SOL = load_solution()


def expected(modules, dependencies):
    mods = [str(x) for x in modules]
    deps = [[str(a), str(b)] for a, b in dependencies]
    return SOL.allBuildOrders(mods, deps)


def fmt_input(modules, dependencies) -> str:
    """与样例同形：["a","b"],[["a","b"]]，紧凑逗号后无空格。"""

    def q(s: str) -> str:
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'

    mpart = "[" + ",".join(q(m) for m in modules) + "]"
    dpart = (
        "["
        + ",".join("[" + q(a) + "," + q(b) + "]" for a, b in dependencies)
        + "]"
    )
    return mpart + "," + dpart


def write_in(path: Path, content: str):
    if content.endswith("\n"):
        content = content.rstrip("\n")
    path.write_bytes(content.encode("utf-8"))


def write_out(path: Path, ans):
    line = json.dumps(ans, separators=(",", ":"), ensure_ascii=False) + "\n"
    path.write_bytes(line.encode("utf-8"))


def write_case(idx: int, modules, dependencies):
    DATA.mkdir(parents=True, exist_ok=True)
    s = fmt_input(modules, dependencies)
    out = expected(modules, dependencies)
    write_in(DATA / f"{idx}.in", s)
    write_out(DATA / f"{idx}.out", out)


def run_std_py_on_in_bytes(raw: bytes) -> str:
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


def build_cases():
    """10 组：前 8 中小，后 2 大；覆盖样例/边界/构造/hack/压力。"""
    big_chain = [f"M{i}" for i in range(1, 101)]
    big_chain_deps = [[big_chain[i], big_chain[i - 1]] for i in range(1, len(big_chain))]

    big_parallel = [f"X{i}" for i in range(1, 41)]
    # X1..X30 为前置层，X31..X40 为后置层，每个后置都依赖所有前置。
    # 这样总拓扑序为 30!/(30!)*10! ? 实际固定为先前置后后置，各层内可任意排列：
    # 共 30! * 10!，过大；因此再加链约束限制为 5! * 5! * 10! 仍很大，不可枚举。
    # 这里改为每层链化，只保留少量可交换点，确保总序列数远小于 10!。
    front = big_parallel[:30]
    back = big_parallel[30:]
    big_parallel_deps = []
    for i in range(1, len(front)):
        big_parallel_deps.append([front[i], front[i - 1]])
    for i in range(1, len(back)):
        big_parallel_deps.append([back[i], back[i - 1]])
    for b in back:
        big_parallel_deps.append([b, front[-1]])

    return [
        (
            ["user", "auth", "database", "api"],
            [["user", "auth"], ["auth", "database"], ["api", "database"]],
        ),
        (["A", "B", "C"], [["A", "B"], ["B", "C"], ["C", "A"]]),
        (
            ["A", "B", "C", "D"],
            [["A", "B"], ["B", "C"], ["C", "D"]],
        ),
        (["a", "b", "c"], []),
        (
            ["A", "B", "C", "D"],
            [["A", "B"], ["A", "C"], ["B", "D"], ["C", "D"]],
        ),
        (["x"], []),
        (["A", "B"], [["A", "B"]]),
        (
            ["C", "A", "B", "D"],
            [["A", "C"], ["B", "C"], ["D", "A"], ["D", "B"]],
        ),
        (big_chain, big_chain_deps),
        (big_parallel, big_parallel_deps),
    ]


def main():
    cases = build_cases()
    assert len(cases) == 10
    for i, (mods, deps) in enumerate(cases, start=1):
        write_case(i, mods, deps)
    verify_all()


if __name__ == "__main__":
    main()
