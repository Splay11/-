def solve(n, A, B, a):
  ca = sum(1 for x in a if x == A)
  cb = sum(1 for x in a if x == B)
  return n * n / (ca * cb)


if __name__ == "__main__":
  n, A, B = map(int, input().split())
  a = list(map(int, input().split()))
  print("%.1f" % solve(n, A, B, a))
