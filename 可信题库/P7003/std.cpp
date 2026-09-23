#include <algorithm>
#include <queue>
#include <vector>
using namespace std;

class Solution {
 public:
  int minFinishTime(int n, vector<int>& prev, vector<int>& next, vector<int>& time) {
    vector<vector<int>> g(n);
    vector<int> indeg(n, 0), finish(n, 0);
    for (size_t i = 0; i < prev.size(); i++) {
      g[prev[i]].push_back(next[i]);
      indeg[next[i]]++;
    }
    queue<int> q;
    for (int i = 0; i < n; i++) {
      if (indeg[i] == 0) {
        finish[i] = time[i];
        q.push(i);
      }
    }
    int seen = 0;
    while (!q.empty()) {
      int u = q.front();
      q.pop();
      seen++;
      for (int v : g[u]) {
        finish[v] = max(finish[v], finish[u] + time[v]);
        if (--indeg[v] == 0) q.push(v);
      }
    }
    if (seen != n) return -1;
    return *max_element(finish.begin(), finish.end());
  }
};
