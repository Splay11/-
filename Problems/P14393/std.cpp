#include <deque>
#include <vector>

using namespace std;

class Solution {
 public:
  vector<int> canIsolateWithTwoPools(vector<int>& resourceCount,
                                     vector<vector<vector<int>>>& conflicts) {
    vector<int> ans;
    // 逐组判断互斥图能否二染色（两池划分）
    for (size_t i = 0; i < resourceCount.size(); i++)
      ans.push_back(bipartite(resourceCount[i], conflicts[i]) ? 1 : 0);
    return ans;
  }

 private:
  bool bipartite(int n, vector<vector<int>>& edges) {
    // 自环：资源不能与自己互斥又同池
    for (auto& e : edges)
      if (e[0] == e[1]) return false;

    // 无向邻接表
    vector<vector<int>> adj(n + 1);
    for (auto& e : edges) {
      int u = e[0], v = e[1];
      adj[u].push_back(v);
      adj[v].push_back(u);
    }

    vector<int> color(n + 1, -1);
    for (int start = 1; start <= n; start++) {
      if (color[start] != -1 || adj[start].empty()) continue;
      color[start] = 0;
      deque<int> q;
      q.push_back(start);
      while (!q.empty()) {
        int u = q.front();
        q.pop_front();
        for (int v : adj[u]) {
          if (color[v] == -1) {
            // 互斥边连接的两个资源必须分到不同池
            color[v] = 1 - color[u];
            q.push_back(v);
          } else if (color[v] == color[u]) {
            // 同色相邻，图含奇环
            return false;
          }
        }
      }
    }
    return true;
  }
};
