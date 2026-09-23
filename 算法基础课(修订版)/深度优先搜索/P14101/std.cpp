#include <iostream>
#include <vector>
using namespace std;

// 全局邻接表，假设节点编号从1到30
vector<int> g[30];
int t; // 终点

// 定义DFS函数
long long dfs(int u){
    // 如果到达终点t，说明找到了一条路径
    if(u == t){
        return 1;
    }
    
    long long res = 0;
    
    // 遍历所有邻接节点并递归计算
    for(auto &v : g[u]){
        res += dfs(v);
    }
    
    return res;
}

int main(){
    int n, m;
    cin >> n >> m;
    
    // 读取边的信息并构建邻接表
    for(int i = 0; i < m; ++i){
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
    }
    
    // 读取起点s和终点t
    int s;
    cin >> s >> t;
    
    // 调用DFS从起点s开始计算路径数量
    long long ans = dfs(s);
    
    // 输出路径数量
    cout << ans;
    
    return 0;
}
