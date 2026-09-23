#include "foo.cc"
#include <cctype>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

static int readInt(const string& s, size_t& i) {
  while (i < s.size() && isspace((unsigned char)s[i])) i++;
  int sign = 1;
  if (i < s.size() && s[i] == '-') {
    sign = -1;
    i++;
  }
  int v = 0;
  bool ok = false;
  while (i < s.size() && isdigit((unsigned char)s[i])) {
    ok = true;
    v = v * 10 + (s[i] - '0');
    i++;
  }
  if (!ok) exit(1);
  return sign * v;
}

static vector<vector<int>> parseArray2d(const string& s, size_t start) {
  size_t i = start;
  while (i < s.size() && isspace((unsigned char)s[i])) i++;
  if (i >= s.size() || s[i] != '[') exit(1);
  i++;
  vector<vector<int>> rows;
  while (true) {
    while (i < s.size() && isspace((unsigned char)s[i])) i++;
    if (i < s.size() && s[i] == ']') {
      i++;
      break;
    }
    if (i >= s.size() || s[i] != '[') exit(1);
    i++;
    vector<int> row;
    while (true) {
      while (i < s.size() && isspace((unsigned char)s[i])) i++;
      if (i < s.size() && s[i] == ']') {
        i++;
        break;
      }
      row.push_back(readInt(s, i));
      while (i < s.size() && isspace((unsigned char)s[i])) i++;
      if (i < s.size() && s[i] == ']') {
        i++;
        break;
      }
      if (i >= s.size() || s[i] != ',') exit(1);
      i++;
    }
    rows.push_back(row);
    while (i < s.size() && isspace((unsigned char)s[i])) i++;
    if (i < s.size() && s[i] == ']') {
      i++;
      break;
    }
    if (i >= s.size() || s[i] != ',') exit(1);
    i++;
  }
  return rows;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string line;
  if (!getline(cin, line)) return 0;
  while (!line.empty() && isspace((unsigned char)line.back())) line.pop_back();
  auto intervals = parseArray2d(line, 0);
  Solution sol;
  cout << sol.countIsolatedIntervals(intervals) << "\n";
  return 0;
}
