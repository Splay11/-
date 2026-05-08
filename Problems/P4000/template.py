import ast
import sys

line = sys.stdin.read().strip()
comma = line.find(",")
if comma < 0:
    raise SystemExit(1)
month = int(line[:comma].strip())
rest = line[comma + 1 :].strip()
split_idx = rest.find("],[")
if split_idx < 0:
    raise SystemExit(1)
employees_str = rest[: split_idx + 1]
birthdays_str = rest[split_idx + 2 :]
employees = ast.literal_eval(employees_str)
birthdays = ast.literal_eval(birthdays_str)
print(Solution().countBirthdayGifts(month, employees, birthdays))
