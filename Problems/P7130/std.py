class Node:
    def __init__(self, val):
        # 双向循环链表的一个节点：值、前驱、后继
        self.val = val
        self.prev = None
        self.next = None


def build_circular(vals):
    """按输入顺序建双向循环链表。空序列返回 None，对应原链表为空。"""
    if not vals:
        return None
    # 先建头节点，再一个个接到尾巴后面
    head = Node(vals[0])
    cur = head
    for v in vals[1:]:
        nxt = Node(v)
        cur.next = nxt
        nxt.prev = cur
        cur = nxt
    # 头尾互连成环：尾的 next 指向头，头的 prev 指向尾
    cur.next = head
    head.prev = cur
    return head


def insert_front(head, x):
    """把头插节点接到循环链表最前面。空表时新节点自己指向自己。"""
    nxt = Node(x)
    if head is None:
        # 空表：插入后只有一个节点，前驱和后继都必须指向自身
        nxt.next = nxt
        nxt.prev = nxt
        return nxt
    # 非空：新节点夹在「原来的尾」和「原来的头」之间
    tail = head.prev
    nxt.next = head
    nxt.prev = tail
    tail.next = nxt
    head.prev = nxt
    return nxt


def traverse(head, cnt):
    """从新头沿后继走 cnt 步，正好一圈（节点数 = 原 n + 1）。"""
    out = []
    cur = head
    for _ in range(cnt):
        out.append(cur.val)
        cur = cur.next
    return out


def insert_and_list(vals, x):
    # 先建原表，再头插，最后沿 next 走一圈输出
    head = build_circular(vals)
    head = insert_front(head, x)
    return traverse(head, len(vals) + 1)


def main():
    # 第一行：原链表长度 n、待插入值 x
    n, x = map(int, input().split())
    if n == 0:
        # n=0 时没有第二行，原链表为空
        vals = []
    else:
        vals = list(map(int, input().split()))
    ans = insert_and_list(vals, x)
    # 用空格拼成一行输出
    print(" ".join(str(v) for v in ans))


if __name__ == "__main__":
    main()
