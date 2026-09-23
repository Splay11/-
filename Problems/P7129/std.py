class Node:
    def __init__(self, val):
        self.val = val
        self.next = None


def build_list(vals):
    """把数组建成单链表，返回头节点。"""
    dummy = Node(0)
    cur = dummy
    for v in vals:
        cur.next = Node(v)
        cur = cur.next
    return dummy.next


def kth_from_end(head, k):
    """快指针先走 k 步，再和慢指针一起走，慢指针停在倒数第 k 个。"""
    fast = head
    for _ in range(k):
        fast = fast.next
    slow = head
    while fast is not None:
        fast = fast.next
        slow = slow.next
    return slow.val


def solve(vals, k):
    head = build_list(vals)
    return kth_from_end(head, k)


def main():
    # 第一行：节点数 n 和倒数序号 k
    n, k = map(int, input().split())
    # 第二行：从头到尾的 n 个节点值
    vals = list(map(int, input().split()))
    print(solve(vals, k))


if __name__ == "__main__":
    main()
