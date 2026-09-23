import ast
import sys


def find_top_level_comma(s):
    """找到两个顶层数组之间的逗号（括号深度为 0 且不在字符串内）。"""
    in_string = False
    bracket = 0
    for i, ch in enumerate(s):
        if ch == '"':
            in_string = not in_string
        elif not in_string:
            if ch == '[':
                bracket += 1
            elif ch == ']':
                bracket -= 1
            elif ch == ',' and bracket == 0:
                return i
    return -1


line = sys.stdin.read().strip()

# 按顶层逗号切分为两个数组，再用 ast 解析为字符串列表
comma = find_top_level_comma(line)
directDeps = ast.literal_eval(line[:comma])
depRules = ast.literal_eval(line[comma + 1:])

result = Solution().getDependencyOrder(directDeps, depRules)

# 按题面样例格式输出：["name:version","name:version",...]（无空格）
print("[" + ",".join('"%s"' % x for x in result) + "]")
