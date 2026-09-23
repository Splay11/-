#include <bits/stdc++.h>
using namespace std;

vector<vector<int> > solve(int r, int c, const vector<vector<int> >& a) {
  // 层和列对调：新表第 j 行第 i 列 = 原表第 i 行第 j 列
  vector<vector<int> > b(c, vector<int>(r));
  for (int j = 0; j < c; j++) {
    for (int i = 0; i < r; i++) {
      b[j][i] = a[i][j];
    }
  }
  return b;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(0);
  int r, c;
  cin >> r >> c;
  vector<vector<int> > a(r, vector<int>(c));
  for (int i = 0; i < r; i++) {
    for (int j = 0; j < c; j++) cin >> a[i][j];
  }
  vector<vector<int> > b = solve(r, c, a);
  for (int j = 0; j < c; j++) {
    for (int i = 0; i < r; i++) {
      if (i) cout << ' ';
      cout << b[j][i];
    }
    cout << "\n";
  }
  return 0;
}
