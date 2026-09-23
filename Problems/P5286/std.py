from collections import Counter


def solve(n, k, a):
  cnt = Counter(a)
  ans = 0
  seen = set()
  for x in cnt:
    if x in seen:
      continue
    y = k - x
    if x == y:
      # 两个相同值即可配成一对，至多保留 1 个
      ans += max(0, cnt[x] - 1)
      seen.add(x)
    elif y in cnt:
      # 完全二部冲突：去掉出现次数较少的一侧
      ans += min(cnt[x], cnt[y])
      seen.add(x)
      seen.add(y)
  return ans


if __name__ == "__main__":
  n, k = map(int, input().split())
  a = list(map(int, input().split()))
  print(solve(n, k, a))
