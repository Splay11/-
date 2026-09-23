class Node:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None


def build_circular(vals):
    """用给定序列建成双向循环链表，返回原头节点。"""
    head = Node(vals[0])
    cur = head
    for v in vals[1:]:
        nxt = Node(v)
        cur.next = nxt
        nxt.prev = cur
        cur = nxt
    # 头尾互连，形成循环
    cur.next = head
    head.prev = cur
    return head


def insert_front(head, x):
    """在循环链表最前面插入值为 x 的新节点，返回新头。"""
    nxt = Node(x)
    tail = head.prev
    # 新节点夹在原来的尾和头之间
    nxt.next = head
    nxt.prev = tail
    tail.next = nxt
    head.prev = nxt
    return nxt


def traverse(head, cnt):
    """从 head 沿后继走 cnt 步，收集节点值。"""
    out = []
    cur = head
    for _ in range(cnt):
        out.append(cur.val)
        cur = cur.next
    return out


def insert_and_list(vals, x):
    head = build_circular(vals)
    head = insert_front(head, x)
    return traverse(head, len(vals) + 1)


def main():
    # 第一行：原链表长度 n 和待插入值 x
    n, x = map(int, input().split())
    # 第二行：从头沿后继走一圈得到的 n 个值
    vals = list(map(int, input().split()))
    ans = insert_and_list(vals, x)
    print(" ".join(str(v) for v in ans))


if __name__ == "__main__":
    main()
