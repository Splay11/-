# -*- coding: utf-8 -*-
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from std import solve

DATA = ROOT / "data"
RNG = random.Random(529420260823)


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


def pack(n, cons):
  lines = [f"{n} {len(cons)}"]
  for typ, a, b, w in cons:
    lines.append(f"{typ} {a} {b} {w}")
  return "\n".join(lines)


def parse(tin):
  lines = tin.split("\n")
  n, m = map(int, lines[0].split())
  cons = []
  for i in range(m):
    parts = lines[1 + i].split()
    cons.append((parts[0], int(parts[1]), int(parts[2]), int(parts[3])))
  return n, cons


def main():
  cases = []

  # 1 改写样例：和差联立已唯一
  cases.append(pack(2, [("S", 1, 2, 8), ("D", 1, 2, 2)]))
  # 2 改写样例：2x=5 无整数解
  cases.append(pack(1, [("S", 1, 1, 5)]))
  # 3 改写样例：差链，一个自由度
  cases.append(pack(3, [("D", 1, 2, 1), ("D", 2, 3, 1)]))
  # 4 边界：自差恒真仍自由；无边孤立点
  cases.append(pack(4, [("D", 1, 1, 0)]))
  # 5 hack：把 S 当 D 会错；S+D 得整数解且已唯一
  cases.append(pack(2, [("S", 1, 2, 20), ("D", 1, 2, 4)]))
  # 6 hack：只数连通块、不看是否钉死；三条和已唯一
  cases.append(pack(3, [("S", 1, 2, 3), ("S", 2, 3, 4), ("S", 1, 3, 5)]))
  # 7 hack：矛盾差账 / 自差非零
  cases.append(pack(3, [("D", 1, 2, 3), ("D", 2, 3, 4), ("D", 1, 3, 1)]))
  # 8 小随机 + 自和偶数钉死 + 大偏移
  cons = [("S", 1, 1, 8), ("D", 2, 3, 1000000000), ("S", 4, 5, -7)]
  for _ in range(8):
    a = RNG.randint(1, 6)
    b = RNG.randint(1, 6)
    if RNG.random() < 0.5:
      cons.append(("D", a, b, RNG.randint(-20, 20)))
    else:
      cons.append(("S", a, b, RNG.randint(-20, 20)))
  cases.append(pack(6, cons))

  # 9 大数据：无边，卡「忘记孤立点各算 1」
  cases.append(pack(100000, []))
  # 10 大数据：差链 + 一条钉死整链的自和 + 若干冗余；卡复杂度与 int 溢出
  n = 100000
  cons = []
  for i in range(1, n):
    cons.append(("D", i, i + 1, 1 if i % 2 == 0 else -1))
  cons.append(("S", 1, 1, 2))  # 钉死整条链；约束恰好 1e5
  cases.append(pack(n, cons))

  assert len(cases) == 10
  for i, tin in enumerate(cases, 1):
    n, cons = parse(tin)
    if n < 1 or n > 100000 or len(cons) > 100000:
      raise RuntimeError(f"bound {i}")
    for typ, a, b, w in cons:
      if typ not in ("D", "S") or not (1 <= a <= n and 1 <= b <= n):
        raise RuntimeError(f"cons {i}")
      if abs(w) > 10**9:
        raise RuntimeError(f"w {i}")
    exp_s, exp_k = solve(n, cons)
    tout = run_std(tin).replace("\r\n", "\n").replace("\r", "\n")
    if not tout.endswith("\n"):
      tout += "\n"
    lines = tout.strip().split("\n")
    if lines[0] != exp_s or int(lines[1]) != exp_k:
      raise RuntimeError(f"mismatch {i}: {lines} vs {exp_s} {exp_k}")
    write_pair(i, tin, tout)
    print(i, exp_s, exp_k, "ok")


if __name__ == "__main__":
  main()
