import sys
import ast


def parse_input(data):
    data = data.strip()
    if not data:
        return "", 0

    try:
        parsed = ast.literal_eval("(" + data + ")")
        if isinstance(parsed, tuple) and len(parsed) == 2:
            return parsed[0], parsed[1]
    except Exception:
        pass

    cleaned = data.replace('"', " ").replace(",", " ")
    parts = cleaned.split()
    if len(parts) < 2:
        return "", 0

    inputStr = parts[0]
    try:
        inputDivisor = int(parts[1])
    except Exception:
        inputDivisor = 0

    return inputStr, inputDivisor


def main():
    data = sys.stdin.read()
    inputStr, inputDivisor = parse_input(data)
    solution = Solution()
    result = solution.getMaxDivisibleNumber(inputStr, inputDivisor)
    print(result)


if __name__ == "__main__":
    main()
