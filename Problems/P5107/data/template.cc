#include "foo.cc"
#include <cctype>
#include <iostream>
#include <string>

using namespace std;

static pair<string, int> parseInput(const string& line) {
    size_t i = 0;
    while (i < line.size() && isspace((unsigned char)line[i])) i++;
    if (i >= line.size() || line[i] != '"') exit(1);
    i++;
    string sn;
    while (i < line.size() && line[i] != '"') sn.push_back(line[i++]);
    if (i >= line.size() || line[i] != '"') exit(1);
    i++;
    if (i >= line.size() || line[i] != ',') exit(1);
    int m = stoi(line.substr(i + 1));
    return {sn, m};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    if (!getline(cin, line)) return 0;
    auto in = parseInput(line);
    Solution sol;
    string ans = sol.rearrangeSN(in.first, in.second);
    cout << '"' << ans << '"' << '\n';
    return 0;
}
