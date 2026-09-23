from collections import defaultdict


def solve(n, k, pairs):
  mp = defaultdict(int)
  for a, b in pairs:
    mp[a] += b
  keys = sorted(mp)
  s = sum(mp.values())
  if s <= k:
    return 0
  for a in keys:
    s -= mp[a]
    if s <= k:
      return a + 1
  return keys[-1] + 1


if __name__ == "__main__":
  n, k = map(int, input().split())
  pairs = [tuple(map(int, input().split())) for _ in range(n)]
  print(solve(n, k, pairs))
