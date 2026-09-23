#include <iostream>
#include <string>
using namespace std;

int solve(string w) {
  // 扫一遍，相邻同色就断开，统计当前段长度
  int best = 1, cur = 1;
  for (int i = 1; i < (int)w.size(); i++) {
    if (w[i] != w[i - 1]) {
      cur++;
      if (cur > best) best = cur;
    } else {
      cur = 1;
    }
  }
  return best;
}

int main() {
  string w;
  cin >> w;
  cout << solve(w) << "\n";
  return 0;
}
