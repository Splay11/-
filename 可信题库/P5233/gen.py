# -*- coding: utf-8 -*-
"""P5233 造数：URI 最长前缀贪心分组计数。"""
from __future__ import annotations

import random
from collections import defaultdict
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(5233)


def count_similar_groups(uri_reqs: List[str]) -> int:
    segs = [u[1:].split("/") for u in uri_reqs]
    remaining = set(range(len(segs)))
    groups = 0
    while True:
        prefix_members = defaultdict(list)
        for i in remaining:
            s = segs[i]
            for L in range(1, len(s) + 1):
                prefix_members[tuple(s[:L])].append(i)
        best_L = 0
        best_key = None
        for pref, mems in prefix_members.items():
            if len(mems) >= 2 and len(pref) > best_L:
                best_L = len(pref)
                best_key = pref
        if best_L == 0:
            break
        for i in prefix_members[best_key]:
            remaining.discard(i)
        groups += 1
    return groups


def fmt_uris(uris: List[str]) -> str:
    return "[" + ", ".join(f'"{u}"' for u in uris) + "]"


def write_case(idx: int, uris: List[str]) -> None:
    assert 2 <= len(uris) <= 200
    assert len(set(uris)) == len(uris)
    for u in uris:
        assert u.startswith("/") and not u.endswith("/")
        assert "//" not in u
        parts = u[1:].split("/")
        assert 1 <= len(parts) <= 20
        assert len(u) <= 300
        for p in parts:
            assert p and all(
                ("a" <= c <= "z") or c.isdigit() or c in "-_" for c in p
            )
    text_in = fmt_uris(uris)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(count_similar_groups(uris)) + "\n")


def rand_seg(max_len: int = 4) -> str:
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789-_"
    L = RNG.randint(1, max_len)
    return "".join(RNG.choice(alphabet) for _ in range(L))


def make_uri(segs: List[str]) -> str:
    return "/" + "/".join(segs)


def rand_unique_uris(n: int, depth_hi: int = 8) -> List[str]:
    seen = set()
    out: List[str] = []
    while len(out) < n:
        d = RNG.randint(1, depth_hi)
        segs = [rand_seg(3) for _ in range(d)]
        u = make_uri(segs)
        if len(u) > 300 or u in seen:
            continue
        seen.add(u)
        out.append(u)
    return out


def tree_uris(branch: int, depth: int) -> List[str]:
    """构造共享前缀的树状 URI，叶子均合法且互异。"""
    out: List[str] = []

    def dfs(path: List[str], d: int) -> None:
        if d == depth:
            out.append(make_uri(path))
            return
        for i in range(branch):
            dfs(path + [f"n{d}x{i}"], d + 1)

    dfs(["root"], 0)
    return out


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    cases: List[List[str]] = []

    # 1-2: 题面样例
    cases.append(
        [
            "/a/b/c/d",
            "/a/b/c",
            "/a/b/d",
            "/a/b/c/d/e",
            "/a/b/c/d/f",
            "/a",
            "/b",
        ]
    )
    cases.append(
        [
            "/aa/b/c",
            "/aa/b/c/d/e",
            "/b/c",
            "/b/c/d",
            "/b",
            "/b/e/o/p/p/r/s/t",
            "/b/d/e",
            "/b/d/h",
        ]
    )

    # 3: 无法成组（首段均不同）
    cases.append(["/a", "/b", "/c", "/d"])

    # 4: 全体共享最长前缀 → 1 组
    cases.append(["/x/y/a", "/x/y/b", "/x/y/c", "/x/y/d"])

    # 5: 两两浅前缀，互不相交 → 2 组（卡「全局只取一对」假解）
    cases.append(["/a/1", "/a/2", "/b/1", "/b/2"])

    # 6: 贪心先取深前缀，浅前缀被拆散（卡「两两配对」）
    # /a/b/c/d 与 /a/b/c/d/e 先成组；/a/b/x 落单 → 1
    cases.append(["/a/b/c/d", "/a/b/c/d/e", "/a/b/x"])

    # 7: 深三元组 + 浅可成组残留
    cases.append(
        [
            "/p/q/r/s",
            "/p/q/r/s/t",
            "/p/q/r/s/u",
            "/p/q/m",
            "/p/q/n",
            "/z",
        ]
    )

    # 8: 同首段大量叶子（L=1 成一组）
    cases.append([f"/s/{i}" for i in range(30)])

    # 9: 树状构造（多轮贪心）
    cases.append(tree_uris(2, 3)[:16])  # root/... 深度结构

    # 10: 接近上限随机
    cases.append(rand_unique_uris(200, depth_hi=12))

    assert len(cases) == 10
    expected = [2, 4, 0, 1, 2, 1, 2, 1]
    for i, uris in enumerate(cases[:8], 1):
        got = count_similar_groups(uris)
        if i <= len(expected):
            assert got == expected[i - 1], (i, got, expected[i - 1], uris)

    for i, uris in enumerate(cases, 1):
        write_case(i, uris)

    # 自校验
    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        uris = eval(raw)
        got = str(count_similar_groups(uris)) + "\n"
        exp = (DATA / f"{i}.out").read_text(encoding="utf-8")
        assert got == exp, (i, got, exp)
        assert not (DATA / f"{i}.in").read_bytes().endswith(b"\n")
        assert (DATA / f"{i}.out").read_bytes().endswith(b"\n")

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
        "主造数脚本：题目根目录 `gen.py`。测例 stdin 为一行字符串数组。\n",
        encoding="utf-8",
    )
    print("P5233 data ok:", [count_similar_groups(c) for c in cases])


if __name__ == "__main__":
    main()
