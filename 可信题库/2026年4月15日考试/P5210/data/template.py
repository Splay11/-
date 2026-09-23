import ast
import sys


def fmt_card(c):
    return "[" + ", ".join(str(x) for x in c) + "]"


def fmt_cards(cards):
    return "[" + ", ".join(fmt_card(c) for c in cards) + "]"


lines = [ln for ln in sys.stdin.read().split("\n") if ln.strip() != ""]
if len(lines) < 2:
    raise SystemExit(0)
cards = ast.literal_eval(lines[0])
align = lines[1].strip()
if len(align) >= 2 and align[0] == '"' and align[-1] == '"':
    align = align[1:-1]
ans = Solution().alignCards(cards, align)
print(fmt_cards(ans))
