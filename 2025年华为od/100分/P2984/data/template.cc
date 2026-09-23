#include "foo.cc"
#include <iostream>
#include <string>

using namespace std;

static bool parseTwoQuoted(const string& line, string& a, string& b) {
    if (line.size() < 5 || line[0] != '"') return false;
    size_t i = 1;
    while (i < line.size() && line[i] != '"') i++;
    if (i >= line.size()) return false;
    a = line.substr(1, i - 1);
    i++;
    while (i < line.size() && (line[i] == ' ' || line[i] == '\t')) i++;
    if (i >= line.size() || line[i] != ',') return false;
    i++;
    while (i < line.size() && (line[i] == ' ' || line[i] == '\t')) i++;
    if (i >= line.size() || line[i] != '"') return false;
    size_t j = ++i;
    while (j < line.size() && line[j] != '"') j++;
    if (j >= line.size()) return false;
    b = line.substr(i, j - i);
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    if (!getline(cin, line)) return 0;
    string a, b;
    if (!parseTwoQuoted(line, a, b)) return 1;
    Solution sol;
    cout << sol.countFormableGroups(a, b) << "\n";
    return 0;
}
