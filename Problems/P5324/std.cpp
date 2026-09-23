#include <iostream>
#include <vector>
using namespace std;

vector<long long> solve(int k, long long t, vector<long long> s) {
  // 在硐口 i 接通后，矿石再走 s[i]，值班员走 t
  // 等待就是多出来的时间，不能为负
  vector<long long> ans(k);
  for (int i = 0; i < k; i++) {
    long long wait = s[i] - t;
    if (wait < 0) wait = 0;
    ans[i] = wait;
  }
  return ans;
}

int main() {
  // 规模较大，关掉同步以免读入拖慢
  ios::sync_with_stdio(false);
  cin.tie(0);
  int k;
  long long t;
  cin >> k >> t;
  vector<long long> s(k);
  for (int i = 0; i < k; i++) cin >> s[i];
  vector<long long> ans = solve(k, t, s);
  for (int i = 0; i < k; i++) {
    if (i) cout << " ";
    cout << ans[i];
  }
  cout << "\n";
  return 0;
}
