#include <bits/stdc++.h>
using namespace std;

long long solve(int n, const vector<pair<pair<int, int>, long long> >& edges) {
  // 只有一个点时无处可走
  if (n == 1) return 0;
  // 建无向树，同时累加全部边权
  vector<vector<pair<int, long long> > > g(n + 1);
  long long total = 0;
  for (size_t i = 0; i < edges.size(); i++) {
    int u = edges[i].first.first;
    int v = edges[i].first.second;
    long long w = edges[i].second;
    g[u].push_back(make_pair(v, w));
    g[v].push_back(make_pair(u, w));
    total += w;
  }
  // 从 1 号队部做一遍遍历，算出到每个哨所的距离
  vector<long long> dist(n + 1, -1);
  dist[1] = 0;
  vector<int> st;
  st.push_back(1);
  while (!st.empty()) {
    int u = st.back();
    st.pop_back();
    for (size_t j = 0; j < g[u].size(); j++) {
      int v = g[u][j].first;
      long long w = g[u][j].second;
      if (dist[v] < 0) {
        dist[v] = dist[u] + w;
        st.push_back(v);
      }
    }
  }
  // 除通往最远哨所的链外，每条边都要走一个来回
  long long farthest = 0;
  for (int i = 1; i <= n; i++) farthest = max(farthest, dist[i]);
  return 2 * total - farthest;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  // 第一行点数，随后 n-1 条边
  int n;
  cin >> n;
  vector<pair<pair<int, int>, long long> > edges;
  for (int i = 0; i < n - 1; i++) {
    int u, v;
    long long w;
    cin >> u >> v >> w;
    edges.push_back(make_pair(make_pair(u, v), w));
  }
  cout << solve(n, edges) << "\n";
  return 0;
}
