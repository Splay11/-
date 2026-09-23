# -*- coding: utf-8 -*-
"""P5475 风控排序评估：10 组测例。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import auc_from_ranks  # noqa: E402

DATA = ROOT / "data"
RNG = random.Random(547520260919)


def fmt_score(x: float) -> str:
    s = "{:.4f}".format(x).rstrip("0").rstrip(".")
    if s == "-0":
        s = "0"
    return s


def write_in(path: Path, labels: list[int], scores: list[float]) -> None:
    lines = [
        str(len(labels)),
        " ".join(str(x) for x in labels),
        " ".join(fmt_score(x) for x in scores),
    ]
    path.write_bytes("\n".join(lines).encode("utf-8"))


def write_out(path: Path, ans: float) -> None:
    path.write_bytes("{:.6f}\n".format(ans).encode("utf-8"))


def dump(idx: int, labels: list[int], scores: list[float]) -> None:
    assert len(labels) == len(scores)
    assert 2 <= len(labels) <= 19
    assert set(labels) <= {0, 1}
    assert 0 in labels and 1 in labels
    auc = auc_from_ranks(labels, scores)
    pair = pairwise_auc(labels, scores)
    if abs(auc - pair) > 1e-12:
        raise SystemExit(f"case {idx}: rank AUC {auc} != pairwise {pair}")
    write_in(DATA / f"{idx}.in", labels, scores)
    write_out(DATA / f"{idx}.out", auc)


def pairwise_auc(labels: list[int], scores: list[float]) -> float:
    pos = [scores[i] for i in range(len(labels)) if labels[i] == 1]
    neg = [scores[i] for i in range(len(labels)) if labels[i] == 0]
    s = 0.0
    for a in pos:
        for b in neg:
            if a > b:
                s += 1.0
            elif a == b:
                s += 0.5
    return s / (len(pos) * len(neg))


def write_config() -> None:
    cases = "\n".join(
        f"      - input: {i}.in\n        output: {i}.out" for i in range(1, 11)
    )
    config = f"""type: default
time: 3s
memory: 512m
subtasks:
  - score: 100
    if: []
    id: 1
    type: sum
    cases:
{cases}
langs:
  - c
  - cc.cc14o2
  - cc
  - java
  - py.py3
  - py
"""
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "config.yaml").write_text(config, encoding="utf-8")
    (ROOT / "config.yaml").write_text(config, encoding="utf-8")


def write_readme() -> None:
    text = """# P5475 测例说明

输入三行：$m$，然后 $m$ 个标签 $t_i$，然后 $m$ 个风险分 $s_i$。输出 AUC，保留 $6$ 位小数。`.in` 末尾无换行，`.out` 末尾恰好一个换行。

分层（每组 10 分）：

- 1：四级样例 1。无并列，单欺诈，$AUC=2/3$。
- 2：四级样例 2。两个 $0.5$ 并列，卡「硬拆名次」。
- 3：$m=2$，完美排序，$AUC=1$。
- 4：$m=2$，完全反序，$AUC=0$。
- 5：全部同分，平均名次后必为 $0.5$。
- 6：多组并列，正负交叉。
- 7：单欺诈、多正常，分数交错。
- 8：随机小数据，含少量并列。
- 9：$m=19$，大块并列压测平均秩。
- 10：$m=19$，接近上限的随机分数与标签。

hack 点：并列不取平均秩、名次从 $0$ 起、按分数降序编号仍套升序公式、并列不算 $0.5$。
"""
    (DATA / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    write_config()
    write_readme()

    dump(1, [0, 0, 0, 1], [0.1, 0.2, 0.9, 0.5])
    dump(2, [0, 1, 1], [0.5, 0.5, 0.8])
    dump(3, [0, 1], [0.2, 0.9])
    dump(4, [1, 0], [0.1, 0.8])
    dump(5, [0, 1, 0, 1], [0.4, 0.4, 0.4, 0.4])
    dump(
        6,
        [0, 1, 0, 1, 0, 1],
        [0.1, 0.1, 0.3, 0.3, 0.7, 0.9],
    )
    dump(
        7,
        [0, 0, 0, 0, 1],
        [0.2, 0.6, 0.6, 0.9, 0.6],
    )
    labels8 = [0, 1, 0, 1, 1, 0, 0]
    scores8 = [0.15, 0.15, 0.4, 0.55, 0.55, 0.8, 0.25]
    dump(8, labels8, scores8)

    labels9 = [0] * 10 + [1] * 9
    RNG.shuffle(labels9)
    if 0 not in labels9:
        labels9[0] = 0
    if 1 not in labels9:
        labels9[-1] = 1
    scores9 = []
    for _ in range(19):
        bucket = RNG.choice([0.1, 0.1, 0.4, 0.4, 0.4, 0.8, 0.8, 1.0])
        scores9.append(bucket)
    dump(9, labels9, scores9)

    labels10 = [RNG.randint(0, 1) for _ in range(19)]
    if 0 not in labels10:
        labels10[0] = 0
    if 1 not in labels10:
        labels10[-1] = 1
    scores10 = [RNG.randrange(0, 21) / 10.0 for _ in range(19)]
    dump(10, labels10, scores10)

    print("generated 10 cases")


if __name__ == "__main__":
    main()
