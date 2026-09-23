/**
 * 特权节点路径 — 到达特权节点后所有边免费
 * 算法：
 * 1. Dijkstra 从起点(0)求最短代价
 * 2. 反向 BFS 从终点(n-1)标记能到达终点的节点
 * 3. 枚举特权节点取最小 dist[p]
 * 复杂度：O((n+m) log n)
 */
#include <iostream>
#include <vector>
#include <queue>
#include <deque>
using namespace std;
using ll = long long;

const ll INF = 1e18;

int main() {
    // 加速 IO
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, k;
    cin >> n >> m >> k;

    // 读入特权节点
    vector<bool> lucky(n);
    vector<int> lucky_nodes;
    lucky_nodes.reserve(k);
    for (int i = 0; i < k; ++i) {
        int r;
        cin >> r;
        --r;  // 转为 0-based
        lucky[r] = true;
        lucky_nodes.push_back(r);
    }

    // 建图：正向图 + 反向图
    vector<vector<pair<int, int>>> g(n);   // 正向 (v, w)
    vector<vector<int>> rg(n);              // 反向（仅存节点）

    for (int i = 0; i < m; ++i) {
        int u, v, w;
        cin >> u >> v >> w;
        --u; --v;  // 转为 0-based
        g[u].push_back({v, w});
        rg[v].push_back(u);  // 反向边
    }

    // ---- 第一步：Dijkstra ----
    vector<ll> dist(n, INF);
    dist[0] = 0;  // 起点为节点 1（下标 0）
    priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<>> pq;
    pq.push({0, 0});

    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d != dist[u]) continue;  // 过期状态，跳过
        for (auto [v, w] : g[u]) {
            ll nd = d + w;
            if (nd < dist[v]) {
                dist[v] = nd;
                pq.push({nd, v});
            }
        }
    }

    // ---- 第二步：反向 BFS ----
    vector<bool> can_reach(n, false);
    can_reach[n - 1] = true;  // 终点自身可达
    deque<int> q;
    q.push_back(n - 1);

    while (!q.empty()) {
        int u = q.front();
        q.pop_front();
        for (int v : rg[u]) {  // 沿反向边走
            if (!can_reach[v]) {
                can_reach[v] = true;
                q.push_back(v);
            }
        }
    }

    // ---- 第三步：枚举特权节点取最小值 ----
    ll ans = INF;
    for (int p : lucky_nodes) {
        if (can_reach[p] && dist[p] < ans) {
            ans = dist[p];
        }
    }

    cout << (ans >= INF ? -1 : ans) << '\n';
    return 0;
}
