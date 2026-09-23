#include <iostream>
#include <string>
#include <vector>
using namespace std;

string solve(int k, vector<int> v) {
  // 贪心：货一到就入栈，栈顶刚好是下一个该出的号就立刻出
  vector<int> st;
  string ops;
  int need = 1;
  for (int i = 0; i < k; i++) {
    st.push_back(v[i]);
    ops += 'I';
    while (!st.empty() && st.back() == need) {
      st.pop_back();
      ops += 'O';
      need++;
    }
  }
  if (need == k + 1) return ops;
  return "N";
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(0);
  int k;
  cin >> k;
  vector<int> v(k);
  for (int i = 0; i < k; i++) cin >> v[i];
  cout << solve(k, v) << "\n";
  return 0;
}
