import json
import sys

line = sys.stdin.read().strip()

# 解析：teamNum,[[matches...]]
comma = line.find(',')
teamNum = int(line[:comma])

rest = line[comma + 1:]
matches = json.loads(rest)

result = Solution().getTopThree(teamNum, matches)

print(json.dumps(result, ensure_ascii=False, separators=(',', ':')))
