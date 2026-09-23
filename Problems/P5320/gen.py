# -*- coding: utf-8 -*-
"""P5320 造数：固定规则感知机。"""
import json
import os
import random

import numpy as np

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DIR, exist_ok=True)


def solve(train, test):
    X = []
    y = []
    for feat, lab in train:
        X.append([1.0] + [float(v) for v in feat])
        y.append(-1.0 if lab == 0 else 1.0)
    X = np.array(X, dtype=float)
    y = np.array(y, dtype=float)
    h = np.zeros(X.shape[1], dtype=float)
    for _ in range(10):
        for i in range(len(X)):
            pred = 1.0 if float(np.dot(h, X[i])) >= 0.0 else -1.0
            if pred != y[i]:
                h = h + y[i] * X[i]
    ans = []
    for feat in test:
        xb = np.array([1.0] + [float(v) for v in feat], dtype=float)
        pred = 1.0 if float(np.dot(h, xb)) >= 0.0 else -1.0
        ans.append(1 if pred == 1.0 else 0)
    return ans


def write_file(idx, obj):
    inn = json.dumps(obj, separators=(",", ":"))
    out = json.dumps(solve(obj["train"], obj["test"]))
    with open(os.path.join(DIR, "%d.in" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write(inn)
    with open(os.path.join(DIR, "%d.out" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write(out + "\n")


def main():
    rng = random.Random(5320)
    write_file(1, {
        "train": [[[0], 0], [[1], 0], [[4], 1], [[5], 1]],
        "test": [[0], [1], [2], [3], [4], [5]],
    })
    write_file(2, {
        "train": [[[0, 0], 0], [[2, 0], 1]],
        "test": [[0, 0], [2, 0], [1, 0]],
    })
    write_file(3, {
        "train": [[[1], 1]],
        "test": [[0], [1], [2]],
    })
    write_file(4, {
        "train": [[[0, 0], 0], [[0, 1], 0], [[1, 0], 1], [[1, 1], 1]],
        "test": [[0, 0], [0, 1], [1, 0], [1, 1]],
    })
    # 5 三维
    write_file(5, {
        "train": [[[0, 0, 0], 0], [[1, 1, 1], 1], [[0, 1, 0], 0]],
        "test": [[0, 0, 0], [1, 1, 1], [0, 1, 1]],
    })
    # 6 更多样本
    train = []
    for i in range(8):
        x = i * 0.5
        train.append([[x], 0 if x < 2 else 1])
    write_file(6, {"train": train, "test": [[0], [1.5], [2], [3], [4]]})
    # 7 随机二维
    tr, te = [], []
    for _ in range(12):
        a, b = rng.random(), rng.random()
        tr.append([[a, b], 1 if a + b > 1 else 0])
    for _ in range(6):
        te.append([rng.random(), rng.random()])
    write_file(7, {"train": tr, "test": te})
    # 8 中等规模
    d = 4
    tr, te = [], []
    for _ in range(30):
        feat = [rng.uniform(-2, 2) for _ in range(d)]
        tr.append([feat, 1 if feat[0] > 0 else 0])
    for _ in range(20):
        te.append([rng.uniform(-2, 2) for _ in range(d)])
    write_file(8, {"train": tr, "test": te})
    # 9 较大
    d = 8
    tr, te = [], []
    for _ in range(80):
        feat = [rng.uniform(-5, 5) for _ in range(d)]
        tr.append([feat, 1 if sum(feat) > 0 else 0])
    for _ in range(40):
        te.append([rng.uniform(-5, 5) for _ in range(d)])
    write_file(9, {"train": tr, "test": te})
    # 10 更大
    d = 10
    tr, te = [], []
    for _ in range(120):
        feat = [rng.uniform(-3, 3) for _ in range(d)]
        tr.append([feat, 1 if feat[-1] >= 0 else 0])
    for _ in range(80):
        te.append([rng.uniform(-3, 3) for _ in range(d)])
    write_file(10, {"train": tr, "test": te})


if __name__ == "__main__":
    main()
