#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

long long solve(int k, long long q, vector<long long> x, vector<long long> y) {
  // 总残差 = sum(x)+sum(y) - q * 进位次数，尽量多配对满足 x+y >= q
  sort(x.begin(), x.end());
  sort(y.begin(), y.end());
  long long sx = 0, sy = 0;
  for (int t = 0; t < k; t++) {
    sx += x[t];
    sy += y[t];
  }
  int i = k - 1, j = 0;
  long long wrap = 0;
  // 从大到小看研发侧，配上还能进位的最小测试侧收益
  while (i >= 0 && j < k) {
    if (x[i] + y[j] >= q) {
      wrap++;
      i--;
      j++;
    } else {
      // 这个测试侧收益连当前最大研发侧都凑不齐
      j++;
    }
  }
  return sx + sy - wrap * q;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(0);
  int k;
  long long q;
  cin >> k >> q;
  vector<long long> x(k), y(k);
  for (int i = 0; i < k; i++) cin >> x[i];
  for (int i = 0; i < k; i++) cin >> y[i];
  cout << solve(k, q, x, y) << "\n";
  return 0;
}
