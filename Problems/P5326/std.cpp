#include <iostream>
#include <string>
using namespace std;

int solve(string w) {
  // 对每个色号，先丢掉比它大的格子，再数它自己的连续段
  int ans = 0;
  for (int c = 0; c < 26; c++) {
    char ch = char('a' + c);
    bool in_run = false;
    for (int i = 0; i < (int)w.size(); i++) {
      char x = w[i];
      if (x > ch) continue;
      if (x == ch) {
        if (!in_run) {
          ans++;
          in_run = true;
        }
      } else {
        // 碰到更小色号，当前段被已经喷好的格子隔开
        in_run = false;
      }
    }
  }
  return ans;
}

int main() {
  string w;
  cin >> w;
  cout << solve(w) << "\n";
  return 0;
}
