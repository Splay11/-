import sys


def parse_input(line: str):
    line = line.strip()
    if not line or line[0] != '"':
        raise SystemExit(1)
    i = 1
    sn_chars = []
    while i < len(line) and line[i] != '"':
        sn_chars.append(line[i])
        i += 1
    if i >= len(line) or line[i] != '"':
        raise SystemExit(1)
    i += 1
    if i >= len(line) or line[i] != ",":
        raise SystemExit(1)
    m = int(line[i + 1 :])
    return "".join(sn_chars), m


line = sys.stdin.read()
if not line.strip():
    raise SystemExit(0)
sn, m = parse_input(line)
ans = Solution().rearrangeSN(sn, m)
print('"' + ans + '"')
