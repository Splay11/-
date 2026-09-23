#include <iostream>
#include <vector>
using namespace std;

const int MOD = 1000000007;
const int MAXK = 200000;

vector<int> precompute() {
  // f1/f2/f3：长度为 i、结尾恰好连续 1/2/3 格同色的方案数
  vector<int> f1(MAXK + 1), f2(MAXK + 1), f3(MAXK + 1), tot(MAXK + 1);
  f1[1] = 26;
  tot[1] = 26;
  for (int i = 2; i <= MAXK; i++) {
    // 换色另起一连
    f1[i] = (int)(1LL * tot[i - 1] * 25 % MOD);
    // 一连延长成两连
    f2[i] = f1[i - 1];
    // 两连延长成三连，不能再变成四连
    f3[i] = f2[i - 1];
    tot[i] = ((f1[i] + f2[i]) % MOD + f3[i]) % MOD;
  }
  return tot;
}

vector<int> solve(const vector<int> &tot, const vector<int> &ks) {
  vector<int> ans(ks.size());
  for (int i = 0; i < (int)ks.size(); i++) ans[i] = tot[ks[i]];
  return ans;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(0);
  int q;
  cin >> q;
  vector<int> ks(q);
  for (int i = 0; i < q; i++) cin >> ks[i];
  vector<int> tot = precompute();
  vector<int> ans = solve(tot, ks);
  for (int i = 0; i < q; i++) cout << ans[i] << "\n";
  return 0;
}
