import ast
import sys


def read_story_literal():
    line = sys.stdin.read()
    if not line:
        return ""
    line = line.strip("\r\n")
    return ast.literal_eval(line)


story = read_story_literal()
print(Solution().lengthOfLongestSubstring(story))
