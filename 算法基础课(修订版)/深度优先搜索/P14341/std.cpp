#include <iostream>
#include <vector>
using namespace std;
#define ll long long
pair<ll, ll> dfs(int node, int father, const vector<vector<int>>& adj, vector<ll>& a) {
    ll totalAdd = 0;
    ll totalSum = 0;
    
    // 处理所有子节点
    for (int child : adj[node]) {
        if (child != father) {
            auto result = dfs(child, node, adj, a);
            totalAdd += result.first;
            totalSum += result.second;
        }
    }
    
    // 确保当前节点的权值大于等于所有子节点的权值和
    if (a[node] < totalSum) {
        totalAdd += totalSum - a[node];
        a[node] = totalSum;  // 更新当前节点的权值
    }
    
    return {totalAdd, a[node]};
}

int main() {
    int n;
    cin >> n;
    vector<ll> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }
    
    vector<pair<int, int>> edges(n - 1);
    for (int i = 0; i < n - 1; i++) {
        cin >> edges[i].first >> edges[i].second;
    }
    vector<vector<int>> adj(n);
    
    // 构建树的邻接表
    for (const auto& edge : edges) {
        adj[edge.first - 1].push_back(edge.second - 1);
        adj[edge.second - 1].push_back(edge.first - 1);
    }
    
    vector<bool> visited(n, false);
    auto result = dfs(0, -1, adj, a);  // 从根节点0开始DFS

    cout << result.first << endl;
    return 0;
}
