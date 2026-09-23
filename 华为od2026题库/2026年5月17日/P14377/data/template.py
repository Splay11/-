import ast
import sys


def parse_input(data):
    data = data.strip()

    # 输入格式：
    # [1, 1, 1, ...], [1, 2, 3, ...]
    colors, numbers = ast.literal_eval(data)

    colors = [int(x) for x in colors]
    numbers = [int(x) for x in numbers]

    return colors, numbers


def main():
    data = sys.stdin.read()
    colors, numbers = parse_input(data)

    ans = Solution().countWinningHands(colors, numbers)
    print(ans)


if __name__ == "__main__":
    main()
