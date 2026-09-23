# -*- coding: utf-8 -*-
import json
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import solve

DATA = ROOT / "data"
RNG = random.Random(528020260824)


def run_std(text):
  r = subprocess.run(
    [sys.executable, str(ROOT / "std.py")],
    input=text.encode(),
    capture_output=True,
    check=True,
  )
  return r.stdout.decode()


def write_pair(idx, tin, tout):
  DATA.mkdir(parents=True, exist_ok=True)
  if tin.endswith("\n"):
    raise RuntimeError("in trailing nl")
  if not tout.endswith("\n") or tout.endswith("\n\n"):
    raise RuntimeError("out nl")
  (DATA / f"{idx}.in").write_bytes(tin.encode())
  (DATA / f"{idx}.out").write_bytes(tout.encode())


def pack(obj):
  return json.dumps(obj, separators=(",", ":"))


def main():
  cases = []
  # 1 改写样例1
  cases.append({
    "train": [[1, 0, 0], [2, 0, 0], [0, 4, 1], [0, 5, 1]],
    "test": [[1, 0], [0, 4], [1, 2]],
    "n_estimators": 2,
    "max_features": 1,
    "seed": 7,
  })
  # 2 改写样例2：三类 + 可能缺类
  cases.append({
    "train": [[0, 0, 0], [1, 0, 0], [0, 1, 1], [8, 8, 2]],
    "test": [[0, 0], [8, 8]],
    "n_estimators": 4,
    "max_features": 2,
    "seed": 1,
  })
  # 3 改写样例3
  cases.append({
    "train": [[3, 1, 0, 0], [3, 2, 0, 0], [1, 3, 1, 1], [1, 4, 1, 1], [9, 9, 9, 2]],
    "test": [[3, 1, 0], [1, 3, 1], [9, 9, 9]],
    "n_estimators": 3,
    "max_features": 2,
    "seed": 13,
  })
  # 4 原题数字全换：两类二维
  cases.append({
    "train": [[1, 1, 0], [1, 2, 0], [8, 8, 1], [8, 9, 1]],
    "test": [[1, 1], [8, 8], [4, 4]],
    "n_estimators": 3,
    "max_features": 1,
    "seed": 3,
  })
  # 5 抽满全部特征
  cases.append({
    "train": [[0, 1, 2, 0], [0, 1, 3, 0], [7, 8, 9, 1]],
    "test": [[0, 1, 2], [7, 8, 9]],
    "n_estimators": 2,
    "max_features": 3,
    "seed": 11,
  })
  # 6 标签不从 0 连续
  cases.append({
    "train": [[0, 0, 2], [1, 0, 2], [0, 5, 5], [1, 6, 5]],
    "test": [[0, 0], [0, 5]],
    "n_estimators": 5,
    "max_features": 1,
    "seed": 21,
  })
  # 7 小随机
  n, d = 8, 4
  train = []
  for i in range(n):
    row = [RNG.randint(0, 6) for _ in range(d)]
    row.append(i % 3)
    train.append(row)
  test = [[RNG.randint(0, 6) for _ in range(d)] for _ in range(5)]
  cases.append({
    "train": train,
    "test": test,
    "n_estimators": 6,
    "max_features": 2,
    "seed": 99,
  })
  # 8 单特征、两类紧挨，卡并列取小编号
  cases.append({
    "train": [[0, 0], [0, 0], [1, 1], [1, 1]],
    "test": [[0], [1], [0.5]],
    "n_estimators": 3,
    "max_features": 1,
    "seed": 8,
  })

  # 9 接近上限：19 条训练、19 条测试、d=9
  n, d = 19, 9
  train = []
  for i in range(n):
    row = [((i * 3 + j) % 11) for j in range(d)]
    row.append(i % 4)
    train.append(row)
  test = [[((i * 5 + j) % 11) for j in range(d)] for i in range(19)]
  cases.append({
    "train": train,
    "test": test,
    "n_estimators": 8,
    "max_features": 4,
    "seed": 2026,
  })
  # 10 稀有类易在袋中缺失
  train = [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 0], [10, 10, 1]]
  test = [[0, 0], [10, 10], [5, 5]]
  cases.append({
    "train": train,
    "test": test,
    "n_estimators": 7,
    "max_features": 1,
    "seed": 42,
  })

  assert len(cases) == 10
  for i, obj in enumerate(cases, 1):
    ntr = len(obj["train"])
    nte = len(obj["test"])
    d = len(obj["train"][0]) - 1
    m = obj["max_features"]
    if not (2 <= ntr <= 19 and 2 <= nte <= 19 and 1 <= d <= 9 and 1 <= m <= d):
      raise RuntimeError(f"bound {i}")
    tin = pack(obj)
    exp = solve(obj)
    exp_s = json.dumps(exp, separators=(",", ":")) + "\n"
    tout = run_std(tin).replace("\r\n", "\n").replace("\r", "\n")
    if not tout.endswith("\n"):
      tout += "\n"
    if json.loads(tout) != exp:
      raise RuntimeError(f"mismatch {i}: {tout} vs {exp_s}")
    if tout != exp_s:
      raise RuntimeError(f"fmt {i}")
    write_pair(i, tin, tout)
    print(i, "ok")


if __name__ == "__main__":
  main()
