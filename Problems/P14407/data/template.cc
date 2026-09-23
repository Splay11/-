#include "foo.cc"
#include <cctype>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

static string readAllInput() {
  string all, chunk;
  while (getline(cin, chunk)) all += chunk;
  while (!all.empty() && isspace((unsigned char)all.back())) all.pop_back();
  return all;
}

static vector<string> parseStringArray(const string& s) {
  vector<string> out;
  size_t i = 0;
  while (i < s.size() && isspace((unsigned char)s[i])) i++;
  if (i >= s.size() || s[i] != '[') exit(1);
  i++;
  while (true) {
    while (i < s.size() && isspace((unsigned char)s[i])) i++;
    if (i < s.size() && s[i] == ']') {
      i++;
      break;
    }
    if (i >= s.size() || s[i] != '"') exit(1);
    i++;
    string val;
    while (i < s.size() && s[i] != '"') val += s[i++];
    if (i >= s.size() || s[i] != '"') exit(1);
    i++;
    out.push_back(val);
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

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string line = readAllInput();
  if (line.empty()) return 0;
  auto commands = parseStringArray(line);
  Solution sol;
  cout << sol.queryNetEnergy(commands) << '\n';
  return 0;
}
