# -*- coding: utf-8 -*-
import random
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(529920260825)


def run_std(text):
  r = subprocess.run(
    ["python", str(ROOT / "std.py")],
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


def pack(n, strs):
  lines = [f"{n} {len(strs)}"] + strs
  return "\n".join(lines)


def rand_s(n):
  return "".join(RNG.choice("ABC") for _ in range(n))


def main():
  cases = []
  cases.append(pack(5, ["CCBAB"]))
  cases.append(pack(5, ["ABCBA"]))
  cases.append(pack(3, ["BAC", "CBA"]))
  cases.append(pack(5, ["CCBAB", "ABCBA"]))
  cases.append(pack(2, ["AA", "AB", "BA", "CC"]))
  cases.append(pack(4, [rand_s(4) for _ in range(20)]))
  cases.append(pack(6, [rand_s(6) for _ in range(50)]))
  cases.append(pack(8, [rand_s(8) for _ in range(200)]))
  cases.append(pack(9, [rand_s(9) for _ in range(500)]))
  cases.append(pack(10, [rand_s(10) for _ in range(2000)]))

  assert len(cases) == 10
  for i, tin in enumerate(cases, 1):
    tout = run_std(tin)
    if not tout.endswith("\n"):
      tout += "\n"
    write_pair(i, tin, tout)
    head = tin.split("\n")[0]
    print(f"{i} ok {head}")


if __name__ == "__main__":
  main()
