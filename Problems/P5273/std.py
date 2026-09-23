def can(limit, dur, days, help_k):
  # 判断主责单日上限为 limit 时，能否在 days 天内按顺序做完
  n = len(dur)
  i = 0
  used = 0
  mask = (1 << 481) - 1  # 支援每天最多 480 分钟，只保留耗时 0..480
  while i < n:
    used += 1
    if used > days:
      return False
    # dp[t] 的第 s 位为 1：当天已交接 t 卷、支援耗时恰好为 s
    dp = [0] * (help_k + 1)
    dp[0] = 1
    total = 0
    last = i - 1
    j = i
    # 贪心尽量延长当天：能接就继续接，直到再加一卷就不合法
    while j < n:
      x = dur[j]
      total += x
      ndp = [0] * (help_k + 1)
      if x <= limit:
        # 这卷主责自己也能做，两种选择都枚举
        for t in range(help_k + 1):
          ndp[t] = dp[t]
          if t > 0:
            ndp[t] |= (dp[t - 1] << x) & mask
      else:
        # 超过主责上限，必须交给支援
        for t in range(1, help_k + 1):
          ndp[t] = (dp[t - 1] << x) & mask
      # 主责耗时 = 当天总和 - 支援耗时，需要 <= limit
      need = total - limit
      if need < 0:
        need = 0
      ok = False
      for t in range(help_k + 1):
        if ndp[t] >> need:
          ok = True
          break
      if not ok:
        break
      dp = ndp
      last = j
      j += 1
    if last < i:
      return False  # 连当前这一卷都排不进任何一天
    i = last + 1
  return True


def solve(n, m, k, dur):
  # 主责每天也最多 480；若上限 480 都排不完则无解
  if not can(480, dur, m, k):
    return -1
  lo, hi = 0, 480
  while lo < hi:
    mid = (lo + hi) // 2
    if can(mid, dur, m, k):
      hi = mid
    else:
      lo = mid + 1
  return lo


if __name__ == "__main__":
  n, m, k = map(int, input().split())
  dur = list(map(int, input().split()))
  print(solve(n, m, k, dur))
