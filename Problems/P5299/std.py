from collections import deque

# 把串编成三进制整数：A=0,B=1,C=2，左边是高位
def encode(s):
  x = 0
  for ch in s:
    x = x * 3 + (ord(ch) - 65)
  return x


# 反转整数状态的前 p 位（左边 p 个字符）
def rev_prefix(x, n, p, pow3):
  digs = [0] * n
  t = x
  for i in range(n - 1, -1, -1):
    digs[i] = t % 3
    t //= 3
  i, j = 0, p - 1
  while i < j:
    digs[i], digs[j] = digs[j], digs[i]
    i += 1
    j -= 1
  y = 0
  for d in digs:
    y = y * 3 + d
  return y


def build_dist(n):
  pw = [1] * (n + 1)
  for i in range(1, n + 1):
    pw[i] = pw[i - 1] * 3
  tot = pw[n]
  dist = [-1] * tot
  q = deque()
  # 所有「若干 A 再若干 B 再若干 C」的串作为起点
  for na in range(n + 1):
    for nb in range(n - na + 1):
      nc = n - na - nb
      x = 0
      for _ in range(na):
        x = x * 3
      for _ in range(nb):
        x = x * 3 + 1
      for _ in range(nc):
        x = x * 3 + 2
      dist[x] = 0
      q.append(x)
  while q:
    x = q.popleft()
    d = dist[x]
    for p in range(2, n + 1):
      y = rev_prefix(x, n, p, pw)
      if dist[y] < 0:
        dist[y] = d + 1
        q.append(y)
  return dist


if __name__ == "__main__":
  n, qn = map(int, input().split())
  dist = build_dist(n)
  out = []
  for _ in range(qn):
    s = input().strip()
    out.append(str(dist[encode(s)]))
  print("\n".join(out))
