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


def rotate_right(head, n, k):
    """把长度为 n 的单链表向右旋转 k 位。"""
    if n == 0 or head is None:
        return None
    k %= n
    if k == 0:
        return head
    # 先走到尾，并收成环，再数 n-k 步断开
    tail = head
    while tail.next is not None:
        tail = tail.next
    tail.next = head
    steps = n - k
    new_tail = head
    for _ in range(steps - 1):
        new_tail = new_tail.next
    new_head = new_tail.next
    new_tail.next = None
    return new_head


def to_list(head):
    out = []
    cur = head
    while cur is not None:
        out.append(cur.val)
        cur = cur.next
    return out


def rotate_vals(vals, k):
    head = build_list(vals)
    head = rotate_right(head, len(vals), k)
    return to_list(head)


def main():
    # 第一行：节点数 n 和旋转次数 k
    n, k = map(int, input().split())
    if n == 0:
        # 空链表输出空行
        print()
        return
    vals = list(map(int, input().split()))
    ans = rotate_vals(vals, k)
    print(" ".join(str(v) for v in ans))


if __name__ == "__main__":
    main()
