#include <bits/stdc++.h>
using namespace std;

struct Node {
  long long d;
  int u, f;
  Node(long long d, int u, int f) : d(d), u(u), f(f) {}
  bool operator>(const Node& o) const { return d > o.d; }
};

long long solve(int n, int F, const vector<int>& p,
                const vector<tuple<int, int, int, int> >& edges) {
  // 建无向图
  vector<vector<tuple<int, int, int> > > g(n + 1);
  for (size_t i = 0; i < edges.size(); i++) {
    int u, v, c, t;
    u = get<0>(edges[i]);
    v = get<1>(edges[i]);
    c = get<2>(edges[i]);
    t = get<3>(edges[i]);
    g[u].push_back(make_tuple(v, c, t));
    g[v].push_back(make_tuple(u, c, t));
  }
  const long long INF = (1LL << 62);
  vector<vector<long long> > dist(n + 1, vector<long long>(F + 1, INF));
  // 出发时满箱
  dist[1][F] = 0;
  priority_queue<Node, vector<Node>, greater<Node> > pq;
  pq.push(Node(0, 1, F));
  while (!pq.empty()) {
    Node cur = pq.top();
    pq.pop();
    long long d = cur.d;
    int u = cur.u, f = cur.f;
    if (d != dist[u][f]) continue;
    if (u == n) return d;
    // 加 1 格电
    if (f < F) {
      long long nd = d + p[u];
      if (nd < dist[u][f + 1]) {
        dist[u][f + 1] = nd;
        pq.push(Node(nd, u, f + 1));
      }
    }
    for (size_t j = 0; j < g[u].size(); j++) {
      int v = get<0>(g[u][j]);
      int c = get<1>(g[u][j]);
      int t = get<2>(g[u][j]);
      if (f >= c) {
        long long nd = d + t;
        int nf = f - c;
        if (nd < dist[v][nf]) {
          dist[v][nf] = nd;
          pq.push(Node(nd, v, nf));
        }
      }
    }
  }
  return -1;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  int n, m, F;
  cin >> n >> m >> F;
  vector<int> p(n + 1);
  for (int i = 1; i <= n; i++) cin >> p[i];
  vector<tuple<int, int, int, int> > edges;
  for (int i = 0; i < m; i++) {
    int u, v, c, t;
    cin >> u >> v >> c >> t;
    edges.push_back(make_tuple(u, v, c, t));
  }
  cout << solve(n, F, p, edges) << "\n";
  return 0;
}
