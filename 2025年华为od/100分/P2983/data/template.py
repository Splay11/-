import sys


def parse_quoted_string(line: str) -> str:
    line = line.strip("\r\n")
    if len(line) >= 2 and line[0] == '"' and line[-1] == '"':
        return line[1:-1]
    return line


raw = sys.stdin.read()
if raw == "":
    raise SystemExit(0)
print(Solution().maxBracketDepth(parse_quoted_string(raw)))
