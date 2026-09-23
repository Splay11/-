# -*- coding: utf-8 -*-
import random
import string
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(529820260825)


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


def pack(s):
  return f"{len(s)}\n{s}"


def rand_s(n, alphabet=None):
  alphabet = alphabet or string.ascii_lowercase
  return "".join(RNG.choice(alphabet) for _ in range(n))


def main():
  cases = []
  cases.append(pack("zyac"))
  cases.append(pack("zyzz"))
  cases.append(pack("xa"))
  cases.append(pack("cccab"))
  cases.append(pack("zzabcz"))
  cases.append(pack("z"))
  cases.append(pack("abc"))
  cases.append(pack(rand_s(50)))
  cases.append(pack("z" * 100 + rand_s(5000)))
  cases.append(pack(rand_s(200000)))

  assert len(cases) == 10
  for i, tin in enumerate(cases, 1):
    tout = run_std(tin)
    if not tout.endswith("\n"):
      tout += "\n"
    write_pair(i, tin, tout)
    n = tin.split("\n")[0]
    print(f"{i} ok n={n} out={tout.strip()[:40]}")


if __name__ == "__main__":
  main()
