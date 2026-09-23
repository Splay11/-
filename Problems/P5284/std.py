import heapq


def solve(n, e, a, b):
  pq = []
  ans = 0
  for i in range(1, n + 1):
    exp = e[i - 1] - 1
    if a[i - 1] > 0 and exp >= i:
      heapq.heappush(pq, [exp, a[i - 1]])
    while pq and pq[0][0] < i:
      heapq.heappop(pq)
    need = b[i - 1]
    while need > 0 and pq:
      if pq[0][0] < i:
        heapq.heappop(pq)
        continue
      take = min(need, pq[0][1])
      pq[0][1] -= take
      need -= take
      if pq[0][1] == 0:
        heapq.heappop(pq)
    ans += need
  return ans


if __name__ == "__main__":
  n = int(input())
  e = list(map(int, input().split()))
  a = list(map(int, input().split()))
  b = list(map(int, input().split()))
  print(solve(n, e, a, b))
