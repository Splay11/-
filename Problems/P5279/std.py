def solve(n, m, a):
  # 默认：单点段长度为 1，变化量记 0，起点 1
  best_len, best_l, best_d = 1, 1, 0
  if n == 1:
    return best_len, best_l, best_d
  i = 0
  while i < n - 1:
    # 从位置 i 开始，看这一段公共变化量
    d = (a[i + 1] - a[i]) % m
    j = i
    while j + 1 < n and (a[j + 1] - a[j]) % m == d:
      j += 1
    # 段 a[i..j]，长度 j-i+1；同样长时保留更靠左的
    cur = j - i + 1
    if cur > best_len:
      best_len, best_l, best_d = cur, i + 1, d
    # 下一段从当前段末尾接着比，避免漏掉交界处
    i = j
  return best_len, best_l, best_d


if __name__ == "__main__":
  n, m = map(int, input().split())
  a = list(map(int, input().split()))
  L, p, d = solve(n, m, a)
  print(L, p, d)
