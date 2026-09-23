import json
import sys

line = sys.stdin.read().strip()
fragments = json.loads(line)
result = Solution().magicFragments(fragments)
print(json.dumps(result, ensure_ascii=False, separators=(',', ':')))
