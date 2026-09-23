import ast
import sys

line = sys.stdin.read().strip()
if line:
    rest = '[' + line + ']'
    cardA, cardB = ast.literal_eval(rest)
    print(Solution().catFishCardGame(cardA, cardB), end="")
