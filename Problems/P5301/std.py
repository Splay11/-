from bisect import bisect_left


def bit_add(c, n, i, v):
  # 树状数组：第 i 档加上 v
  while i <= n:
    c[i] += v
    i += i & -i


def bit_sum(c, i):
  # 树状数组：前 i 档前缀和
  s = 0
  while i:
    s += c[i]
    i -= i & -i
  return s


def solve_one(n, a, ops):
  # 初始值和所有修改值一起离散化
  vals = list(a)
  for op in ops:
    if op[0] == 1:
      vals.append(op[2])
  xs = sorted(set(vals))
  m = len(xs)
  cnt = [0] * (m + 1)
  sm = [0] * (m + 1)

  def idx(x):
    return bisect_left(xs, x) + 1

  def pair_with(x):
    # 比它小：个数*x-和；比它大：和-个数*x；相等贡献为 0
    i = idx(x)
    cnt_lt = bit_sum(cnt, i - 1)
    sum_lt = bit_sum(sm, i - 1)
    cnt_le = bit_sum(cnt, i)
    sum_le = bit_sum(sm, i)
    cnt_all = bit_sum(cnt, m)
    sum_all = bit_sum(sm, m)
    cnt_gt = cnt_all - cnt_le
    sum_gt = sum_all - sum_le
    return cnt_lt * x - sum_lt + sum_gt - cnt_gt * x

  s = 0
  arr = list(a)
  for x in arr:
    # 先插入再累加，不会和自己配对
    i = idx(x)
    bit_add(cnt, m, i, 1)
    bit_add(sm, m, i, x)
    s += pair_with(x)

  out = []
  for op in ops:
    if op[0] == 2:
      out.append(s)
    else:
      p, y = op[1] - 1, op[2]
      old = arr[p]
      # 树里还留着旧值时先扣贡献，再替换
      s -= pair_with(old)
      i = idx(old)
      bit_add(cnt, m, i, -1)
      bit_add(sm, m, i, -old)
      arr[p] = y
      i = idx(y)
      bit_add(cnt, m, i, 1)
      bit_add(sm, m, i, y)
      s += pair_with(y)
  return out


if __name__ == "__main__":
  T = int(input())
  ans = []
  for _ in range(T):
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    ops = []
    for _ in range(m):
      ops.append(tuple(map(int, input().split())))
    ans.extend(solve_one(n, a, ops))
  print("\n".join(map(str, ans)))
