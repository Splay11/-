class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build_list(vals):
    dummy = ListNode(0)
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def list_to_vals(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def reverse_between(head, left, right):
    # 哑节点方便处理 left=1 的情况
    dummy = ListNode(0, head)
    pre = dummy
    for _ in range(left - 1):
        pre = pre.next
    # pre 后是待反转区间起点；头插法把后续节点插到 pre 后面
    cur = pre.next
    for _ in range(right - left):
        nxt = cur.next
        cur.next = nxt.next
        nxt.next = pre.next
        pre.next = nxt
    return dummy.next


def main():
    n, left, right = map(int, input().split())
    vals = list(map(int, input().split()))
    head = reverse_between(build_list(vals[:n]), left, right)
    print(*list_to_vals(head))


if __name__ == "__main__":
    main()
