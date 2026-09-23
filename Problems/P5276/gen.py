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
RNG = random.Random(527620260822)


def run_std(obj):
  text = json.dumps(obj, separators=(",", ":"))
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


def rand_p():
  return round(RNG.uniform(0.0, 1.0), 2)


def make_case(n, m):
  cal_y = [RNG.randint(0, 1) for _ in range(n)]
  cal_p1 = [rand_p() for _ in range(n)]
  test_p1 = [rand_p() for _ in range(m)]
  return {"cal_y": cal_y, "cal_p1": cal_p1, "test_p1": test_p1}


def main():
  cases = []
  cases.append({
    "cal_y": [0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
    "cal_p1": [0.05, 0.10, 0.15, 0.20, 0.95, 0.90, 0.85, 0.80, 0.75, 0.30],
    "test_p1": [0.0, 1.0, 0.5, 0.2, 0.8],
  })
  cases.append(make_case(5, 4))
  cases.append(make_case(8, 6))
  cases.append(make_case(3, 3))
  cases.append({
    "cal_y": [0, 1, 0],
    "cal_p1": [0.01, 0.99, 0.02],
    "test_p1": [0.0, 1.0, 0.5],
  })
  cases.append(make_case(12, 10))
  cases.append(make_case(15, 8))
  cases.append(make_case(18, 15))
  cases.append(make_case(6, 12))
  cases.append({
    "cal_y": [1, 0, 1, 0, 1],
    "cal_p1": [0.9, 0.1, 0.8, 0.2, 0.7],
    "test_p1": [0.95, 0.05, 0.5, 0.5, 0.5, 0.5],
  })

  assert len(cases) == 10
  for i, obj in enumerate(cases, 1):
    n, m = len(obj["cal_y"]), len(obj["test_p1"])
    assert 3 <= n <= 19 and 2 <= m <= 19
    solve(obj["cal_y"], obj["cal_p1"], obj["test_p1"])
    tin = json.dumps(obj, separators=(",", ":"))
    tout = run_std(obj)
    if not tout.endswith("\n"):
      tout += "\n"
    write_pair(i, tin, tout)
    print(f"{i} ok n={n} m={m}")


if __name__ == "__main__":
  main()
