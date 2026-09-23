import json
import sys

line = sys.stdin.read().strip()

comma = line.find(',')
splitLine = int(line[:comma])

rest = line[comma + 1:]
sqlText = json.loads(rest)

print(Solution().splitSQLToFiles(splitLine, sqlText))
