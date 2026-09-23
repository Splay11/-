#include <bits/stdc++.h>
using namespace std;

vector<pair<int, int> > solve(int n, const vector<pair<int, int> >& edges) {
  // 无向无权图：邻接表存双向边
  vector<vector<int> > g(n + 1);
  for (size_t i = 0; i < edges.size(); i++) {
    int u = edges[i].first, v = edges[i].second;
    g[u].push_back(v);
    g[v].push_back(u);
  }
  // dist[i] = -1 表示还没走到；门厅 1 号距离为 0
  vector<int> dist(n + 1, -1);
  dist[1] = 0;
  queue<int> q;
  q.push(1);
  while (!q.empty()) {
    int u = q.front();
    q.pop();
    for (size_t j = 0; j < g[u].size(); j++) {
      int v = g[u][j];
      if (dist[v] < 0) {
        dist[v] = dist[u] + 1;
        q.push(v);
      }
    }
  }
  // 只收集可达点，按（距离，编号）排序
  vector<pair<int, int> > arr;
  for (int i = 1; i <= n; i++) {
    if (dist[i] >= 0) arr.push_back(make_pair(dist[i], i));
  }
  sort(arr.begin(), arr.end());
  return arr;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(0);
  int n, m;
  cin >> n >> m;
  vector<pair<int, int> > edges;
  for (int i = 0; i < m; i++) {
    int u, v;
    cin >> u >> v;
    edges.push_back(make_pair(u, v));
  }
  vector<pair<int, int> > ans = solve(n, edges);
  for (size_t i = 0; i < ans.size(); i++) {
    // 输出：编号 距离
    cout << ans[i].second << " " << ans[i].first << "\n";
  }
  return 0;
}
