import sys


def parse_quoted_string(line: str) -> str:
    line = line.strip("\r\n")
    if len(line) >= 2 and line[0] == '"' and line[-1] == '"':
        return line[1:-1]
    return line


line = sys.stdin.read()
if not line.strip():
    raise SystemExit(0)
s = parse_quoted_string(line)
print(Solution().countOpenSyllables(s))
