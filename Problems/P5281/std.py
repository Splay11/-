MAXM = 1001
THRESH = 500

n = int(input())
w = [0] * n
a = [0] * n
b = [0] * n
for i in range(n):
  wi, ai, bi = map(int, input().split())
  w[i] = wi
  a[i] = ai
  b[i] = bi

prefixB = [0] * (n + 1)
suffixB = [0] * (n + 1)
for i in range(n):
  prefixB[i + 1] = prefixB[i] + b[i]
for i in range(n - 1, -1, -1):
  suffixB[i] = suffixB[i + 1] + b[i]

f = [[0] * MAXM for _ in range(n + 1)]
for m in range(MAXM):
  f[n][m] = m

for i in range(n - 1, -1, -1):
  wi, ai, bi = w[i], a[i], b[i]
  sb = suffixB[i + 1]
  fi1 = f[i + 1]
  row = f[i]
  for m in range(MAXM):
    if wi < m:
      nm = m - bi
      if nm < 0:
        nm = 0
    else:
      nm = m + ai
    if nm < MAXM:
      row[m] = fi1[nm]
    elif nm - sb > THRESH:
      row[m] = nm - sb
    else:
      j = i
      cur = nm
      while j < n and cur > THRESH:
        cur -= b[j]
        j += 1
      row[m] = cur if j >= n else f[j][cur]


def apply_from(i, money):
  if i >= n:
    return money
  if money > THRESH and money - suffixB[i] > THRESH:
    return money - suffixB[i]
  if money < MAXM:
    return f[i][money]
  j = i
  cur = money
  while j < n and cur > THRESH:
    cur -= b[j]
    j += 1
  return cur if j >= n else f[j][cur]


def answer(x):
  if x < MAXM:
    return f[0][x]
  if x - suffixB[0] > THRESH:
    return x - suffixB[0]
  lo, hi = 0, n
  while lo < hi:
    mid = (lo + hi + 1) // 2
    if x - prefixB[mid] > THRESH:
      lo = mid
    else:
      hi = mid - 1
  i = lo
  money = x - prefixB[i]
  if i >= n:
    return money
  return apply_from(i, money)


q = int(input())
out = []
for _ in range(q):
  out.append(str(answer(int(input()))))
print("\n".join(out))
