#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
using namespace std;

// 最少波次 = DAG 上最长链包含的模型个数
int minWaves(int p, const vector<pair<int, int>>& rel) {
    vector<vector<int>> graph(p + 1);
    vector<int> indeg(p + 1, 0);
    for (size_t k = 0; k < rel.size(); k++) {
        int u = rel[k].first;
        int v = rel[k].second;
        graph[u].push_back(v);
        indeg[v]++;
    }

    // dp[x]：以 x 结尾的最长链长度；孤立点为 1
    vector<int> dp(p + 1, 1);
    queue<int> q;
    for (int i = 1; i <= p; i++) {
        if (indeg[i] == 0) {
            q.push(i);
        }
    }

    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (int v : graph[u]) {
            // 先走完 u 再走 v，链长至少是 dp[u] + 1
            dp[v] = max(dp[v], dp[u] + 1);
            indeg[v]--;
            if (indeg[v] == 0) {
                q.push(v);
            }
        }
    }

    int ans = 1;
    for (int i = 1; i <= p; i++) {
        ans = max(ans, dp[i]);
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int p, e;
    cin >> p >> e;
    vector<pair<int, int>> rel;
    rel.reserve(e);
    // 每条约束：v 等 u，对应有向边 u -> v
    for (int k = 0; k < e; k++) {
        int u, v;
        cin >> u >> v;
        rel.push_back({u, v});
    }
    cout << minWaves(p, rel) << "\n";
    return 0;
}
