def can_reach(n, a, m, k, x):
  # 差分数组记录「区间加」何时失效；add 是扫到当前位置时已经叠加的次数
  diff = [0] * (n + 1)
  add = 0
  used = 0
  for i in range(n):
    add += diff[i]
    need = x - a[i] - add
    if need > 0:
      used += need
      if used > m:
        return False
      # 贪心：区间左端钉在 i，尽量盖满长度为 k 的窗口
      add += need
      end = i + k
      if end < n:
        diff[end] -= need
  return True


def solve(n, m, k, a):
  # 二分最终的最小值：下界是当前最小，上界是再把 m 次全加到最小段
  lo = min(a)
  hi = lo + m
  ans = lo
  while lo <= hi:
    mid = (lo + hi) // 2
    if can_reach(n, a, m, k, mid):
      ans = mid
      lo = mid + 1
    else:
      hi = mid - 1
  return ans


if __name__ == "__main__":
  # 第一行 n,m,k，第二行 n 个平整度
  n, m, k = map(int, input().split())
  a = list(map(int, input().split()))
  print(solve(n, m, k, a))
