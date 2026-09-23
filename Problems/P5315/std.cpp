#include <iostream>
#include <vector>
using namespace std;

vector<int> solve(int p, int s, vector<long long> r) {
  // 单调栈求左右最近的不低于自己的测站
  vector<int> left(p, -1), right(p, p);
  vector<int> st;
  for (int i = 0; i < p; i++) {
    while (!st.empty() && r[st.back()] < r[i]) st.pop_back();
    if (!st.empty()) left[i] = st.back();
    st.push_back(i);
  }
  st.clear();
  for (int i = p - 1; i >= 0; i--) {
    while (!st.empty() && r[st.back()] < r[i]) st.pop_back();
    if (!st.empty()) right[i] = st.back();
    st.push_back(i);
  }
  vector<int> peaks;
  for (int i = 0; i < p; i++) {
    // 半径 s 内不能出现 >= r[i] 的其他测站
    bool ok_l = left[i] < 0 || i - left[i] > s;
    bool ok_r = right[i] >= p || right[i] - i > s;
    if (ok_l && ok_r) peaks.push_back(i + 1);
  }
  return peaks;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(0);
  int p, s;
  cin >> p >> s;
  vector<long long> r(p);
  for (int i = 0; i < p; i++) cin >> r[i];
  vector<int> peaks = solve(p, s, r);
  cout << peaks.size() << "\n";
  for (int i = 0; i < (int)peaks.size(); i++) {
    if (i) cout << " ";
    cout << peaks[i];
  }
  cout << "\n";
  return 0;
}
