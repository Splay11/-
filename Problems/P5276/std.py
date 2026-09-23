import json
import math
import sys

import numpy as np


def solve(cal_y, cal_p1, test_p1, alpha=0.2):
  """Split Conformal 分类预测集 → 整数标签。"""
  cal_y = np.asarray(cal_y, dtype=int)
  cal_p1 = np.asarray(cal_p1, dtype=float)
  test_p1 = np.asarray(test_p1, dtype=float)

  # 非一致性分数：正类 s=1-p，负类 s=p
  s = np.where(cal_y == 1, 1.0 - cal_p1, cal_p1)
  s_sorted = np.sort(s)
  n = len(cal_y)
  k = math.ceil((n + 1) * (1 - alpha)) - 1
  if k >= n:
    k = n - 1
  q = float(s_sorted[k])

  out = []
  for p in test_p1:
    in0 = p <= q
    in1 = p >= 1.0 - q
    if in0 and in1:
      out.append(-1)
    elif in0:
      out.append(0)
    elif in1:
      out.append(1)
    else:
      out.append(-2)
  return out


def main():
  data = json.loads(sys.stdin.read())
  cal_y = data["cal_y"]
  cal_p1 = data["cal_p1"]
  test_p1 = data["test_p1"]
  result = solve(cal_y, cal_p1, test_p1)
  sys.stdout.write(json.dumps(result))


if __name__ == "__main__":
  main()
