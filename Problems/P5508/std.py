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


def odd_even_list(head):
    if not head or not head.next:
        return head
    # odd/even 分别串奇数位与偶数位，最后偶数链接到奇数链尾
    odd, even = head, head.next
    even_head = even
    while even and even.next:
        odd.next = even.next
        odd = odd.next
        even.next = odd.next
        even = even.next
    odd.next = even_head
    return head


def main():
    n = int(input())
    if n == 0:
        print()
        return
    vals = list(map(int, input().split()))
    head = odd_even_list(build_list(vals[:n]))
    ans = list_to_vals(head)
    if ans:
        print(*ans)
    else:
        print()


if __name__ == "__main__":
    main()
