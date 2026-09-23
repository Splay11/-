import sys

line = sys.stdin.readline().strip()
if line:
    parts = line.split(',')
    M = int(parts[0].strip())
    N = int(parts[1].strip())

    s = Solution()
    print(s.getNthValue(M, N), end='')
