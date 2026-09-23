from collections import defaultdict

def main():
    # 读取节点数和边数
    n, m = map(int, input().split())
    
    # 初始化邻接表
    g = defaultdict(list)
    
    # 读取边的信息并构建邻接表
    for _ in range(m):
        u, v = map(int, input().split())
        g[u].append(v)
    
    # 读取起点s和终点t
    s, t = map(int, input().split())
    
    def dfs(u):
        """
        递归函数，计算从节点u到终点t的路径数
        """
        # 如果到达终点t，说明找到了一条路径
        if u == t:
            return 1
        
        # 初始化路径数量
        res = 0
        
        # 遍历所有邻接节点并递归计算
        for v in g[u]:
            res += dfs(v)
        
        return res

    # 调用dfs从起点s开始计算路径数量
    ans = dfs(s)
    
    # 输出路径数量
    print(ans)

if __name__ == '__main__':
    main()
