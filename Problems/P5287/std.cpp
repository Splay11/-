#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll INF = (ll)4e18;

vector<ll> dijkstra(int n, const vector<vector<pair<int, int>>>& g, int src) {
  vector<ll> dist(n + 1, INF);
  priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<pair<ll, int>>> pq;
  dist[src] = 0;
  pq.push({0, src});
  while (!pq.empty()) {
    auto [d, u] = pq.top();
    pq.pop();
    if (d != dist[u]) continue;
    for (auto [v, w] : g[u]) {
      if (d + w < dist[v]) {
        dist[v] = d + w;
        pq.push({dist[v], v});
      }
    }
  }
  return dist;
}

int main() {
  int n, m, k, s;
  cin >> n >> m >> k >> s;
  vector<vector<pair<int, int>>> g(n + 1);
  for (int i = 0; i < m; i++) {
    int u, v, w;
    cin >> u >> v >> w;
    g[u].push_back({v, w});
  }
  for (int i = 0; i < k; i++) {
    int u, v, w;
    cin >> u >> v >> w;
    g[u].push_back({v, w});
    g[v].push_back({u, w});
  }
  int a, b, q;
  cin >> a >> b >> q;
  vector<int> dest(q);
  for (int i = 0; i < q; i++) cin >> dest[i];

  vector<int> uniq;
  unordered_set<int> seen;
  auto add = [&](int x) {
    if (!seen.count(x)) {
      seen.insert(x);
      uniq.push_back(x);
    }
  };
  add(s);
  for (int x : dest) add(x);

  unordered_map<int, vector<ll>> table;
  for (int u : uniq) table[u] = dijkstra(n, g, u);

  ll t = 0;
  int cur = s;
  for (int d : dest) {
    t += table[cur][d];
    if (t % 2 == 1) t += a;
    else t += b;
    cur = d;
  }
  t += table[cur][s];
  cout << t << "\n";
  return 0;
}
