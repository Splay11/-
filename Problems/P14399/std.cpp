#include <algorithm>
#include <unordered_map>
#include <vector>

using namespace std;

class Solution {
 public:
  int maxZoneImbalance(vector<int>& loads, vector<vector<int>>& edges) {
    int n = (int)loads.size();
    if (edges.empty()) return -1;
    vector<int> parent(n);
    for (int i = 0; i < n; i++) parent[i] = i;
    auto find = [&](int x) {
      while (parent[x] != x) {
        parent[x] = parent[parent[x]];
        x = parent[x];
      }
      return x;
    };
    auto unite = [&](int a, int b) {
      a = find(a);
      b = find(b);
      if (a != b) parent[b] = a;
    };
    for (auto& e : edges) unite(e[0], e[1]);
    unordered_map<int, vector<int>> groups;
    for (int i = 0; i < n; i++) groups[find(i)].push_back(i);
    int ans = -1;
    for (auto& kv : groups) {
      auto& nodes = kv.second;
      if ((int)nodes.size() < 2) continue;
      int mn = loads[nodes[0]], mx = loads[nodes[0]];
      for (int id : nodes) {
        mn = min(mn, loads[id]);
        mx = max(mx, loads[id]);
      }
      ans = max(ans, (mx - mn) * (int)nodes.size());
    }
    return ans;
  }
};
