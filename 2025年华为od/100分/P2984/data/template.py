import re
import sys


def parse_two_quoted(line: str):
    line = line.strip("\r\n")
    m = re.fullmatch(r'"(.*)"\s*,\s*"(.*)"', line)
    if not m:
        raise SystemExit("bad input")
    return m.group(1), m.group(2)


raw = sys.stdin.read()
if not raw.strip():
    raise SystemExit(0)
a, b = parse_two_quoted(raw)
print(Solution().countFormableGroups(a, b))
