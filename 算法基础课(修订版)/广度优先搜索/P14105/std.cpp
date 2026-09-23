#include <iostream>
#include <vector>
#include <queue>

using namespace std;

void bfs(int start, vector<vector<int>>& adj, vector<bool>& visited) {
    queue<int> q;
    q.push(start);
    visited[start] = true;

    while (!q.empty()) {
        int node = q.front();
        q.pop();

        // 遍历所有相邻节点
        for (int neighbor : adj[node]) {
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                q.push(neighbor);
            }
        }
    }
}

int main() {
    int n, m;
    cin >> n >> m;

    // 邻接表存储图
    vector<vector<int>> adj(n + 1);
    vector<bool> visited(n + 1, false);

    // 读取图的边
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);  // 无向图双向连接
    }

    int connectedComponents = 0;

    // 对每个节点进行BFS遍历
    for (int i = 1; i <= n; i++) {
        if (!visited[i]) {
            bfs(i, adj, visited);
            connectedComponents++;  // 每找到一个连通块，计数加1
        }
    }

    cout << connectedComponents << endl;
    return 0;
}
