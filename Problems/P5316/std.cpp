#include <iostream>
#include <set>
#include <vector>
using namespace std;

vector<long long> solve(int w, vector<long long> v, vector<vector<long long> > caps,
                        vector<vector<long long> > floors) {
  // 稀释闸 [L,R] 上界 c：L 加入，R+1 删除
  vector<vector<long long> > add_c(w + 2), del_c(w + 2), add_d(w + 2), del_d(w + 2);
  for (int i = 0; i < (int)caps.size(); i++) {
    add_c[(int)caps[i][0]].push_back(caps[i][2]);
    del_c[(int)caps[i][1] + 1].push_back(caps[i][2]);
  }
  for (int i = 0; i < (int)floors.size(); i++) {
    add_d[(int)floors[i][0]].push_back(floors[i][2]);
    del_d[(int)floors[i][1] + 1].push_back(floors[i][2]);
  }
  // 可重集合维护当前上界最小值、下界最大值
  multiset<long long> hc, hd;
  const long long inf = 1000000000000000000LL;
  vector<long long> e(w);
  for (int i = 1; i <= w; i++) {
    for (int j = 0; j < (int)del_c[i].size(); j++) hc.erase(hc.find(del_c[i][j]));
    for (int j = 0; j < (int)add_c[i].size(); j++) hc.insert(add_c[i][j]);
    for (int j = 0; j < (int)del_d[i].size(); j++) hd.erase(hd.find(del_d[i][j]));
    for (int j = 0; j < (int)add_d[i].size(); j++) hd.insert(add_d[i][j]);
    long long hi = hc.empty() ? inf : *hc.begin();
    long long lo = hd.empty() ? 0 : *hd.rbegin();
    long long val = v[i - 1];
    if (val < lo) val = lo;
    if (val > hi) val = hi;
    e[i - 1] = val;
  }
  return e;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(0);
  int w, x, y;
  cin >> w >> x >> y;
  vector<long long> v(w);
  for (int i = 0; i < w; i++) cin >> v[i];
  vector<vector<long long> > caps(x, vector<long long>(3));
  for (int i = 0; i < x; i++) cin >> caps[i][0] >> caps[i][1] >> caps[i][2];
  vector<vector<long long> > floors(y, vector<long long>(3));
  for (int i = 0; i < y; i++) cin >> floors[i][0] >> floors[i][1] >> floors[i][2];
  vector<long long> e = solve(w, v, caps, floors);
  for (int i = 0; i < w; i++) {
    if (i) cout << " ";
    cout << e[i];
  }
  cout << "\n";
  return 0;
}
