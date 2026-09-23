import sys

line = sys.stdin.read()
if not line.strip():
    raise SystemExit(0)
header = line.strip("\r\n")
print(Solution().parsePacketHeader(header))
