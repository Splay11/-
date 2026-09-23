import ast
import re
import sys


def parse_room_arrangement(text):
    text = text.strip()
    if not text:
        return []
    try:
        data = ast.literal_eval(text)
    except Exception:
        text = re.sub(r"(?<=\[|,)\s*([.#])\s*(?=,|\])", r"'\1'", text)
        data = ast.literal_eval(text)
    return [[str(cell) for cell in row] for row in data]


def main():
    text = sys.stdin.read()
    room_arrangement = parse_room_arrangement(text)
    answer = Solution().networkPlanning(room_arrangement)
    sys.stdout.write(str(answer))


if __name__ == "__main__":
    main()
