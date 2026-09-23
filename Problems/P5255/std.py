def can_queue(u, v):
    return u == v


def can_stack(u, v):
    st = []
    i = 0
    n = len(u)
    # 按出站序列贪心：栈顶不匹配就继续入站
    for c in v:
        while i < n and (not st or st[-1] != c):
            st.append(u[i])
            i += 1
        if not st or st[-1] != c:
            return False
        st.pop()
    return True


def solve(u, v):
    q = can_queue(u, v)
    s = can_stack(u, v)
    if q and s:
        return "both"
    if q:
        return "queue"
    if s:
        return "stack"
    return "neither"


u = input().strip()
v = input().strip()
print(solve(u, v))
