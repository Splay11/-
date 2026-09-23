INF = 10 ** 18 + 5


def add(a, b):
  s = a + b
  if s > INF:
    return INF
  return s


def solve(m, q, b):
  # ways0[L]/ways1[L]：长度为 L、开头为 0/1 的明暗交错子序列个数
  ways0 = [0] * (m + 1)
  ways1 = [0] * (m + 1)
  pre0 = [0] * (m + 1)
  pre1 = [0] * (m + 1)
  for i in range(m):
    cur = [0] * (m + 1)
    cur[1] = 1
    # 接到相反色的更短段后面，保证相邻不同
    if b[i] == "0":
      for L in range(2, i + 2):
        cur[L] = pre1[L - 1]
    else:
      for L in range(2, i + 2):
        cur[L] = pre0[L - 1]
    for L in range(1, i + 2):
      # 结尾色固定，长度奇偶决定开头色
      if L % 2 == 1:
        start = b[i]
      else:
        start = "1" if b[i] == "0" else "0"
      if start == "0":
        ways0[L] = add(ways0[L], cur[L])
      else:
        ways1[L] = add(ways1[L], cur[L])
    if b[i] == "0":
      for L in range(1, i + 2):
        pre0[L] = add(pre0[L], cur[L])
    else:
      for L in range(1, i + 2):
        pre1[L] = add(pre1[L], cur[L])
  # 空串最短，名次至少从 2 起，先扣掉空串
  q -= 1
  for L in range(1, m + 1):
    for start, cnt in ((0, ways0[L]), (1, ways1[L])):
      if q <= cnt:
        t = []
        bit = start
        for _ in range(L):
          t.append(str(bit))
          bit = 1 - bit
        return "".join(t)
      q -= cnt
  return "-1"


m, q = map(int, input().split())
b = input().strip()
print(solve(m, q, b))
