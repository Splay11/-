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

static vector<string> parseStringArray(const string& s, size_t start) {
  vector<string> out;
  size_t i = start;
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

static vector<string> splitTopLevel(const string& line) {
  vector<string> parts;
  size_t start = 0;
  int depth = 0;
  bool inStr = false;
  for (size_t i = 0; i < line.size(); i++) {
    char c = line[i];
    if (inStr) {
      if (c == '"') inStr = false;
      continue;
    }
    if (c == '"') {
      inStr = true;
    } else if (c == '[') {
      depth++;
    } else if (c == ']') {
      depth--;
    } else if (c == ',' && depth == 0) {
      parts.push_back(line.substr(start, i - start));
      start = i + 1;
    }
  }
  parts.push_back(line.substr(start));
  return parts;
}

static void printArray(const vector<int>& a) {
  cout << '[';
  for (size_t k = 0; k < a.size(); k++) {
    if (k) cout << ',';
    cout << a[k];
  }
  cout << ']' << '\n';
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string line = readAllInput();
  if (line.empty()) return 0;
  auto parts = splitTopLevel(line);
  if (parts.size() < 2) exit(1);
  auto logs = parseStringArray(parts[0], 0);
  auto keywords = parseStringArray(parts[1], 0);
  Solution sol;
  printArray(sol.analyzeLogKeywords(logs, keywords));
  return 0;
}
