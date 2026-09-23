#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

long long pick_median(vector<pair<long long, long long> > pts) {
  // 按坐标排序后，累加人数，找到加权中位数
  sort(pts.begin(), pts.end());
  long long tot = 0;
  for (int i = 0; i < (int)pts.size(); i++) tot += pts[i].second;
  long long acc = 0;
  for (int i = 0; i < (int)pts.size(); i++) {
    acc += pts[i].second;
    // 前缀人数第一次达到总人数的一半，就是最优落点
    if (acc * 2 >= tot) return pts[i].first;
  }
  return pts.back().first;
}

long long solve(int m, vector<long long> a, vector<long long> b, vector<long long> w) {
  vector<pair<long long, long long> > xs, ys;
  for (int i = 0; i < m; i++) {
    xs.push_back(make_pair(a[i], w[i]));
    ys.push_back(make_pair(b[i], w[i]));
  }
  // 横、纵分别取加权中位数
  long long P = pick_median(xs);
  long long Q = pick_median(ys);
  long long ans = 0;
  for (int i = 0; i < m; i++) {
    long long dx = a[i] - P;
    if (dx < 0) dx = -dx;
    long long dy = b[i] - Q;
    if (dy < 0) dy = -dy;
    ans += w[i] * (dx + dy);
  }
  return ans;
}

int main() {
  int m;
  cin >> m;
  vector<long long> a(m), b(m), w(m);
  for (int i = 0; i < m; i++) cin >> a[i] >> b[i] >> w[i];
  cout << solve(m, a, b, w) << endl;
  return 0;
}
