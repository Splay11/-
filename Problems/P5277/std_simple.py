# 朴素：每次修改后 sort(set(b)) 扫相邻半距
n, m = map(int, input().split())
b = list(map(int, input().split()))


def calc_w(arr):
  u = sorted(set(arr))
  ans = 0
  for i in range(len(u) - 1):
    ans = max(ans, (u[i + 1] - u[i]) // 2)
  return ans


for _ in range(m):
  r, z = map(int, input().split())
  b[r - 1] = z
  print(calc_w(b))
