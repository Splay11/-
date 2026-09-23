
import sys

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def build_list(nums):
    dummy = ListNode(0)
    cur = dummy
    for x in nums:
        cur.next = ListNode(x)
        cur = cur.next
    return dummy.next

def parse_nums(s):
    s = s.strip()
    if len(s) < 2:
        return []
    s = s.strip("{}")
    if not s.strip():
        return []
    return [int(x.strip()) for x in s.split(",") if x.strip()]

line = sys.stdin.read().strip()
nums = parse_nums(line)
head = build_list(nums)

ans = Solution().gameResult(head)

# 输出文件要求带双引号，这里统一补外层双引号
print('"' + str(ans) + '"', end='')
