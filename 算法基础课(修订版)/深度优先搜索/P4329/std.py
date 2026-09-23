MOD = 10**9 + 7

def cc(a, b, t):
    """ 根据运算类型 t 计算当前节点的权值 """
    return (a + b) % MOD if t == 0 else (a * b) % MOD

def cal(u):
    """ 递归计算节点 u 的权值 """
    if len(adj[u]) == 2:  # 非叶子节点，递归计算左右子节点的值
        return cc(cal(adj[u][0]), cal(adj[u][1]), ops[u])
    return 1  # 叶子节点权值固定为 1

# 读取输入
num = int(input().strip())
tree_info = list(map(int, input().split()))
ops = list(map(int, input().split()))

# 构建邻接表
adj = [[] for _ in range(num)]
for i in range(num - 1):
    parent = tree_info[i] - 1  # 转换为 0 索引
    child = i + 1
    adj[parent].append(child)

# 输出根节点的计算结果
print(cal(0))
