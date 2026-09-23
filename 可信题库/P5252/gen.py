# -*- coding: utf-8 -*-
"""P5252 造数：预算内最优带宽套餐。"""
from __future__ import annotations

import json
import random
import shutil
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(5252)

Case = Tuple[List[List[int]], int]


def best_bandwidth(packages: List[List[int]], budget: int) -> int:
    best_bw = -1
    best_price = None
    for bw, price in packages:
        if price > budget:
            continue
        if best_bw < 0 or bw > best_bw or (bw == best_bw and price < best_price):
            best_bw = bw
            best_price = price
    return best_bw


def fmt_packages(packages: List[List[int]]) -> str:
    if len(packages) <= 10:
        parts = []
        for bw, price in packages:
            parts.append(f"[{bw}, {price}]")
        return "[" + ", ".join(parts) + "]"
    return json.dumps(packages, separators=(",", ":"))


def write_case(idx: int, packages: List[List[int]], budget: int) -> None:
    assert 0 <= len(packages) <= 10**4
    assert 0 <= budget <= 10**9
    for p in packages:
        assert len(p) == 2
        assert 1 <= p[0] <= 10**9
        assert 1 <= p[1] <= 10**9
    text_in = fmt_packages(packages) + "\n" + str(budget)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(best_bandwidth(packages, budget)) + "\n")


def rand_pkg(n: int) -> List[List[int]]:
    return [[RNG.randint(1, 10**9), RNG.randint(1, 10**9)] for _ in range(n)]


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases: List[Case] = []

    # 1-3: 题面样例
    cases.append(([[100, 50], [200, 120], [150, 80]], 100))
    cases.append(([[300, 200], [100, 50]], 40))
    cases.append(([[100, 60], [100, 40], [80, 30]], 60))

    # 4: 空套餐
    cases.append(([], 100))

    # 5: budget=0，价格至少为 1，全买不起
    cases.append(([[10, 1], [20, 1]], 0))

    # 6: 恰等于预算边界
    cases.append(([[50, 100], [80, 100], [90, 101]], 100))

    # 7: 同带宽多价格，应选更便宜对应的带宽（仍返回带宽）
    cases.append(([[200, 90], [200, 50], [150, 40]], 100))

    # 8: 中等随机
    cases.append((rand_pkg(200), RNG.randint(0, 10**9)))

    # 9: 大：多数买不起，末尾有一个最优
    pkgs9 = [[RNG.randint(1, 1000), RNG.randint(10**8, 10**9)] for _ in range(9999)]
    pkgs9.append([999999999, 1])
    cases.append((pkgs9, 10))

    # 10: 大：同带宽多价格 hack（错误取第一个而非最便宜）
    pkgs10 = [[5000, RNG.randint(100, 500)] for _ in range(5000)]
    pkgs10 += [[5000, 50], [4999, 1], [6000, 10**9]]
    cases.append((pkgs10, 1000))

    assert len(cases) == 10
    assert best_bandwidth(*cases[0]) == 150
    assert best_bandwidth(*cases[1]) == -1
    assert best_bandwidth(*cases[2]) == 100
    assert best_bandwidth(*cases[5]) == 80
    assert best_bandwidth(*cases[6]) == 200

    for i, (packages, budget) in enumerate(cases, 1):
        write_case(i, packages, budget)

    import importlib.util

    spec = importlib.util.spec_from_file_location("std_mod", ROOT / "std.py")
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)
    sol = std_mod.Solution()

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        lines = raw.split("\n")
        assert len(lines) == 2
        packages = json.loads(lines[0])
        budget = int(lines[1])
        got = str(sol.bestBandwidth(packages, budget)) + "\n"
        exp = (DATA / f"{i}.out").read_text(encoding="utf-8")
        assert got == exp, (i, got, exp)
        assert not (DATA / f"{i}.in").read_bytes().endswith(b"\n")
        assert (DATA / f"{i}.out").read_bytes().endswith(b"\n")
        assert (DATA / f"{i}.out").read_bytes().count(b"\n") == 1

    cases_yaml = "\n".join(
        f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11)
    )
    config = f"""type: default
user_extra_files:
  - template.py
  - template.java
  - template.cc
  - compile.sh
  - config.yaml
  - user.cc
  - user.java
  - user.py
subtasks:
  - score: 100
    if: []
    id: 1
    type: sum
    cases:
{cases_yaml}
langs:
  - py.py3
  - java
  - cc.cc14o2
  - py
  - cc
"""
    (DATA / "config.yaml").write_text(config, encoding="utf-8")
    (DATA / "README.md").write_text(
        "主造数脚本：题目根目录 `gen.py`。stdin 两行：packages / budget。\n",
        encoding="utf-8",
    )
    compile_src = Path(r"d:\机考出题\problem-maker\compile.sh")
    shutil.copyfile(compile_src, DATA / "compile.sh")
    print("P5252 data ok:", [best_bandwidth(*c) for c in cases])


if __name__ == "__main__":
    main()
