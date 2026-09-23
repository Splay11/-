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

static vector<int> parseArray1d(const string& s, size_t& i) {
  while (i < s.size() && isspace((unsigned char)s[i])) i++;
  if (i >= s.size() || s[i] != '[') exit(1);
  i++;
  vector<int> vals;
  while (true) {
    while (i < s.size() && isspace((unsigned char)s[i])) i++;
    if (i < s.size() && s[i] == ']') {
      i++;
      break;
    }
    vals.push_back(readInt(s, i));
    while (i < s.size() && isspace((unsigned char)s[i])) i++;
    if (i < s.size() && s[i] == ']') {
      i++;
      break;
    }
    if (i >= s.size() || s[i] != ',') exit(1);
    i++;
  }
  return vals;
}

static vector<vector<int>> parseArray2d(const string& s, size_t& i) {
  while (i < s.size() && isspace((unsigned char)s[i])) i++;
  if (i >= s.size() || s[i] != '[') exit(1);
  i++;
  vector<vector<int>> out;
  while (true) {
    while (i < s.size() && isspace((unsigned char)s[i])) i++;
    if (i < s.size() && s[i] == ']') {
      i++;
      break;
    }
    out.push_back(parseArray1d(s, i));
    while (i < s.size() && isspace((unsigned char)s[i])) i++;
    if (i < s.size() && s[i] == ']') {
      i++;
      break;
    }
    if (i >= s.size() || s[i] != ',') exit(1);
    i++;
  }
  return out;
}

static vector<string> splitTopLevel(const string& line) {
  vector<string> parts;
  size_t start = 0;
  int depth = 0;
  for (size_t i = 0; i < line.size(); i++) {
    if (line[i] == '[') depth++;
    else if (line[i] == ']') depth--;
    else if (line[i] == ',' && depth == 0) {
      parts.push_back(line.substr(start, i - start));
      start = i + 1;
    }
  }
  parts.push_back(line.substr(start));
  return parts;
}

static void printAnswer(const vector<vector<int>>& ans) {
  cout << '[';
  for (size_t i = 0; i < ans.size(); i++) {
    if (i) cout << ',';
    cout << '[';
    for (size_t j = 0; j < ans[i].size(); j++) {
      if (j) cout << ',';
      cout << ans[i][j];
    }
    cout << ']';
  }
  cout << "]\n";
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string line;
  if (!getline(cin, line)) return 0;
  while (!line.empty() && isspace((unsigned char)line.back())) line.pop_back();
  auto parts = splitTopLevel(line);
  int n = stoi(parts[0]);
  int k = stoi(parts[1]);
  size_t pos = 0;
  auto weights = parseArray1d(parts[2], pos);
  pos = 0;
  auto conflicts = parseArray2d(parts[3], pos);
  Solution sol;
  printAnswer(sol.selectMaxWeightPolicies(n, k, weights, conflicts));
  return 0;
}
