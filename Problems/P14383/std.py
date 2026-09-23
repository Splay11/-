# -*- coding: utf-8 -*-
from typing import List


class Solution:
  def countValidPlans(self, timestamps: List[int], minInterval: int) -> int:
    ts = sorted(timestamps)
    n = len(ts)
    ans = 0
    for mask in range(1 << n):
      ok = True
      picked = []
      for i in range(n):
        if mask & (1 << i):
          picked.append(ts[i])
      for i in range(len(picked)):
        for j in range(i + 1, len(picked)):
          if picked[j] - picked[i] < minInterval:
            ok = False
            break
        if not ok:
          break
      if ok:
        ans += 1
    return ans
