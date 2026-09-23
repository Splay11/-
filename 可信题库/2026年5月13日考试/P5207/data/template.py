import sys


def parse_quoted(line: str) -> str:
    line = line.strip()
    if len(line) >= 2 and line[0] == '"' and line[-1] == '"':
        return line[1:-1]
    return line


line = sys.stdin.read()
if not line.strip():
    raise SystemExit(0)
code = parse_quoted(line.strip("\r\n"))
ans = Solution().flipWorkId(code)
print('"' + ans + '"')
