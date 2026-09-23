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


def delete_duplicates(head):
    # 哑节点，方便删掉头上的重复段
    dummy = ListNode(0, head)
    pre = dummy
    while pre.next:
        cur = pre.next
        # 当前值出现重复则整段删除
        if cur.next and cur.next.val == cur.val:
            x = cur.val
            while pre.next and pre.next.val == x:
                pre.next = pre.next.next
        else:
            pre = pre.next
    return dummy.next


def main():
    n = int(input())
    if n == 0:
        print()
        return
    vals = list(map(int, input().split()))
    head = delete_duplicates(build_list(vals[:n]))
    ans = list_to_vals(head)
    if ans:
        print(*ans)
    else:
        print()


if __name__ == "__main__":
    main()
