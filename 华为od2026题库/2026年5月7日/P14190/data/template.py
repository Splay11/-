import re
import sys

from typing import List


data = list(map(int, re.findall(r"\d+", sys.stdin.read())))
if not data:
    sys.exit(0)

optimize = data[-1]
goodProceeTime = data[:-1]

print(Solution().minProcessTime(goodProceeTime, optimize))
