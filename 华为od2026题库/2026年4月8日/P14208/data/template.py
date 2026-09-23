import ast
import sys

def main():
    line = sys.stdin.read().strip()
    if not line:
        return
    data = ast.literal_eval("[" + line + "]")
    month = data[0]
    employees = data[1]
    birthdays = data[2]
    result = Solution().countBirthdayGifts(month, employees, birthdays)
    print(result, end="")

if __name__ == "__main__":
    main()
