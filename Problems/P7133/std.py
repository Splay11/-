def solve(importance, children, start):
    """从 start 出发走完整棵下属树，把沿途每人的重要度加起来。
    用栈做 DFS，避免链状组织把递归撑爆（n 可以到 2000）。
    """
    total = 0
    stack = [start]
    while stack:
        u = stack.pop()
        total += importance[u]
        # 把直属下属压栈，之后会继续走到间接下属
        for v in children[u]:
            stack.append(v)
    return total


def solve_from_employees(employees, qid):
    # employees 里每一项是 (员工id, 重要度, 直属下属id列表)
    importance = {}
    children = {}
    for eid, imp, subs in employees:
        importance[eid] = imp
        children[eid] = list(subs)
    return solve(importance, children, qid)


def main():
    # 第一行：员工人数 n、要查询的员工 id
    n, qid = map(int, input().split())
    employees = []
    for _ in range(n):
        parts = list(map(int, input().split()))
        eid = parts[0]
        imp = parts[1]
        m = parts[2]
        # m=0 时这一行到此结束，没有下属 id
        subs = parts[3:3 + m]
        employees.append((eid, imp, subs))
    print(solve_from_employees(employees, qid))


if __name__ == "__main__":
    main()
