import sys
import json


def parse_quoted_string(s: str) -> str:
    """提取引号内的字符串"""
    start = s.find('"')
    end = s.rfind('"')
    if start == -1 or end == -1 or start >= end:
        return ""
    return s[start + 1:end]


def parse_int_list(s: str) -> list:
    """解析整型数组 [a,b,c,...]"""
    s = s.strip()
    if s.startswith('[') and s.endswith(']'):
        inner = s[1:-1]
        if inner.strip() == "":
            return []
        return [int(x.strip()) for x in inner.split(',')]
    return []


# 读取整行输入
line = sys.stdin.read().strip()

# 解析输入: "CIDR",N,[requirements]
# 找到第一个顶层逗号
bracket_depth = 0
in_string = False
comma1 = -1
for i, c in enumerate(line):
    if c == '"':
        in_string = not in_string
    elif not in_string:
        if c == '[':
            bracket_depth += 1
        elif c == ']':
            bracket_depth -= 1
        elif c == ',' and bracket_depth == 0:
            comma1 = i
            break

cidr = parse_quoted_string(line[:comma1])

rest = line[comma1 + 1:]

# 第二个顶层逗号
bracket_depth = 0
in_string = False
comma2 = -1
for i, c in enumerate(rest):
    if c == '"':
        in_string = not in_string
    elif not in_string:
        if c == '[':
            bracket_depth += 1
        elif c == ']':
            bracket_depth -= 1
        elif c == ',' and bracket_depth == 0:
            comma2 = i
            break

n = int(rest[:comma2].strip())
requirements = parse_int_list(rest[comma2 + 1:].strip())

# 调用用户代码
result = Solution().allocateSubnets(cidr, n, requirements)

# 输出结果
print("[" + ",".join('"' + r + '"' for r in result) + "]")
