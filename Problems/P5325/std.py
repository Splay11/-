MOD = 1000000007
MAXK = 200000


def precompute():
  # f1/f2/f3：长度为 i、结尾恰好连续 1/2/3 格同色的方案数
  f1 = [0] * (MAXK + 1)
  f2 = [0] * (MAXK + 1)
  f3 = [0] * (MAXK + 1)
  tot = [0] * (MAXK + 1)
  f1[1] = 26
  tot[1] = 26
  for i in range(2, MAXK + 1):
    # 换一种与最后一格不同的色号，结尾连续变成 1
    f1[i] = tot[i - 1] * 25 % MOD
    # 把结尾一连再涂一格相同色，变成两连
    f2[i] = f1[i - 1]
    # 把结尾两连再涂一格相同色，变成三连
    f3[i] = f2[i - 1]
    tot[i] = (f1[i] + f2[i] + f3[i]) % MOD
  return tot


def solve(tot, ks):
  # 每条灯带直接查预处理表
  return [tot[k] for k in ks]


tot = precompute()
q = int(input())
ks = []
for _ in range(q):
  ks.append(int(input()))
ans = solve(tot, ks)
for x in ans:
  print(x)
