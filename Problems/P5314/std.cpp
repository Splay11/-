#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

long long solve(int k, int u, int v, long long g, vector<long long> h) {
  // 渗水量从大到小排：封堵令给最大的，引流令给接下来的
  sort(h.begin(), h.end(), greater<long long>());
  long long ans = 0;
  for (int i = 0; i < k; i++) {
    if (i < u) {
      // 封堵，该点残留为 0
      continue;
    }
    if (i < u + v) {
      // 引流，减去固定幅度 g，不能减成负数
      long long val = h[i] - g;
      if (val < 0) val = 0;
      ans += val;
    } else {
      // 暂缓，残留就是原渗水量
      ans += h[i];
    }
  }
  return ans;
}

int main() {
  // 规模较大，关掉同步以免读入拖慢
  ios::sync_with_stdio(false);
  cin.tie(0);
  int k, u, v;
  long long g;
  cin >> k >> u >> v >> g;
  vector<long long> h(k);
  for (int i = 0; i < k; i++) cin >> h[i];
  cout << solve(k, u, v, g, h) << "\n";
  return 0;
}
