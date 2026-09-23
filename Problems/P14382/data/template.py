import ast
import sys


def read_expr_literal():
    line = sys.stdin.read()
    if not line:
        return ""
    line = line.strip("\r\n")
    return ast.literal_eval(line)


input_str = read_expr_literal()
print(Solution().processExpression(input_str))
