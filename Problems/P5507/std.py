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


def reorder_list(head):
    if not head or not head.next:
        return head
    # 快慢指针找中点，拆成前后两段
    slow, fast = head, head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    second = slow.next
    slow.next = None
    # 反转后半段
    prev = None
    while second:
        nxt = second.next
        second.next = prev
        prev = second
        second = nxt
    # 交错合并
    first, second = head, prev
    while second:
        n1, n2 = first.next, second.next
        first.next = second
        second.next = n1
        first, second = n1, n2
    return head


def main():
    n = int(input())
    vals = list(map(int, input().split()))
    head = reorder_list(build_list(vals[:n]))
    print(*list_to_vals(head))


if __name__ == "__main__":
    main()
