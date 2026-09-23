import sys

rules = sys.stdin.readline().rstrip('\n')
s = Solution()
print(s.getErrorCount(rules))
