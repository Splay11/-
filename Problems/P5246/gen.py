# -*- coding: utf-8 -*-
"""生成 P5246 的 data/*.in/*.out。

规则：
- .in 末尾无多余换行（紧凑单行 JSON，与样例输入同形）
- .out 末尾恰有一个换行（json.dumps 默认空格风格，与样例输出同形）
- 前 8 组小数据，后 2 组接近 n=24、每条 4 项上限
"""

from __future__ import annotations

import json
import random
from itertools import combinations
from pathlib import Path

SEED = 524620260815
RNG = random.Random(SEED)
ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
N_MAX = 24
LEN_MAX = 4


def support_of(itemset, recs):
    s = set(itemset)
    return sum(1 for r in recs if s <= r)


def frequent_itemsets(records, min_cnt):
    recs = [set(r) for r in records]
    cnt = {}
    for r in recs:
        for x in r:
            cnt[x] = cnt.get(x, 0) + 1
    G = sorted((x,) for x, c in cnt.items() if c >= min_cnt)
    U = []
    while G:
        G_set = set(G)
        k = len(G[0])
        for itemset in G:
            U.append([list(itemset), support_of(itemset, recs)])
        D = []
        for i in range(len(G)):
            for j in range(i + 1, len(G)):
                a, b = G[i], G[j]
                if a[:-1] == b[:-1] and a[-1] < b[-1]:
                    cand = a + (b[-1],)
                    ok = all(sub in G_set for sub in combinations(cand, k))
                    if ok:
                        D.append(cand)
        G = [cand for cand in D if support_of(cand, recs) >= min_cnt]
        G.sort()
    U.sort(key=lambda x: (len(x[0]), x[0]))
    return U


def validate(records, min_cnt):
    n = len(records)
    assert 1 <= n <= N_MAX
    assert isinstance(min_cnt, int) and min_cnt >= 1
    for r in records:
        assert 0 <= len(r) <= LEN_MAX
        assert len(r) == len(set(r))
        assert all(isinstance(x, int) for x in r)


def fmt_in(records, min_cnt):
    obj = {"records": records, "min_cnt": min_cnt}
    return json.dumps(obj, separators=(",", ":"))


def fmt_out(ans):
    return json.dumps(ans) + "\n"


def build_cases():
    cases = []

    def add(desc, records, min_cnt):
        validate(records, min_cnt)
        ans = frequent_itemsets(records, min_cnt)
        cases.append((desc, fmt_in(records, min_cnt), fmt_out(ans)))

    add(
        "样例1：二元项集部分被阈值丢掉",
        [[1, 2], [1, 2], [1, 3], [2, 3]],
        2,
    )
    add(
        "样例2：三元频繁项集存活",
        [[2, 3, 5], [2, 3, 5], [2, 3], [3, 5]],
        2,
    )
    add("边界：n=1、单项、min_cnt=1", [[7]], 1)
    add(
        "边界：min_cnt>n，结果为空；含空记录",
        [[1, 2], [], [3]],
        4,
    )
    add(
        "hack：子集计数而非整条记录相等（{1,2} 被 {1,2,3} 包含）",
        [[1, 2, 3], [1, 2, 3], [1, 2]],
        2,
    )
    add(
        "hack：编号按数值字典序（2<10<11，不能当字符串比）",
        [[2, 10], [2, 10], [10, 11], [2, 11], [2, 10, 11]],
        2,
    )
    add(
        "hack：同支持的真子集也要输出（非极大/非闭项集）",
        [[1, 2], [1, 2], [1, 2], [1, 2]],
        2,
    )
    recs8 = []
    for _ in range(10):
        k = RNG.randint(1, 4)
        recs8.append(sorted(RNG.sample(range(1, 9), k)))
    recs8[0] = [1]
    recs8[1] = [8, 1, 4]
    add("随机小数据：n=10，编号 1..8", recs8, 2)

    universe9 = [1, 2, 3, 4, 5, 6]
    recs9 = []
    for i in range(N_MAX):
        recs9.append(sorted(RNG.sample(universe9, LEN_MAX)))
    recs9[0] = [1, 2, 3, 4]
    recs9[-1] = [3, 4, 5, 6]
    add("大数据：n=24，全集 6 个编号、每条 4 项，min_cnt=8", recs9, 8)

    recs10 = []
    for i in range(N_MAX):
        pool = list(range(1, 13))
        k = LEN_MAX
        recs10.append(RNG.sample(pool, k))
    recs10[0] = [12, 1, 7, 3]
    recs10[1] = [2, 10, 11, 4]
    recs10[2] = [1, 2, 3, 4]
    add("大数据：n=24 拉满，记录无序，min_cnt=1", recs10, 1)

    assert len(cases) == 10
    return cases


def write_cases(cases):
    DATA.mkdir(parents=True, exist_ok=True)
    readme_lines = [
        "# P5246 测试数据说明",
        "",
        "输入为紧凑单行 JSON（键 `records` / `min_cnt`），与改写题面样例同形。",
        "约束：$1\\le n\\le 24$，每条记录互异整数且长度 $\\le 4$，$\\textit{min\\_cnt}\\ge 1$。",
        "",
        "| 编号 | 类型 | 说明 | 针对的错误解 |",
        "|---:|---|---|---|",
    ]
    tags = [
        "样例",
        "样例",
        "边界",
        "边界",
        "hack",
        "hack",
        "hack",
        "随机",
        "构造/压力",
        "构造/压力",
    ]
    hacks = [
        "—",
        "—",
        "漏掉 n=1 / 单项",
        "min_cnt 大于出现次数仍输出项集；空记录当非法",
        "用记录相等代替子集包含",
        "把编号当字符串排序",
        "只输出极大项集或闭项集",
        "随机噪声下计数/排序漂移",
        "层数到 4、候选剪枝与计数",
        "min_cnt=1 时项集多、记录无序",
    ]
    for i, ((desc, in_text, out_text), tag, hack) in enumerate(
        zip(cases, tags, hacks), 1
    ):
        (DATA / f"{i}.in").write_bytes(in_text.encode("utf-8"))
        (DATA / f"{i}.out").write_bytes(out_text.encode("utf-8"))
        readme_lines.append(f"| {i} | {tag} | {desc} | {hack} |")
    (DATA / "README.md").write_bytes(("\n".join(readme_lines) + "\n").encode("utf-8"))


def self_check(cases):
    for i, (desc, in_text, out_text) in enumerate(cases, 1):
        assert not in_text.endswith("\n"), f"case {i}: .in 不应以换行结尾"
        assert out_text.endswith("\n") and not out_text.endswith("\n\n"), (
            f"case {i}: .out 换行规则"
        )
        obj = json.loads(in_text)
        got = fmt_out(frequent_itemsets(obj["records"], obj["min_cnt"]))
        if got != out_text:
            raise SystemExit(
                f"自检失败：第 {i} 组（{desc}）\n期望:\n{out_text!r}\n得到:\n{got!r}"
            )


def main():
    cases = build_cases()
    write_cases(cases)
    self_check(cases)
    print(f"已生成 {len(cases)} 组数据到 {DATA}")


if __name__ == "__main__":
    main()
