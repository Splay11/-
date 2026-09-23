#include "foo.cc"
#include <cctype>
#include <iostream>
#include <string>

using namespace std;

static string parseQuotedString(const string& s) {
    size_t i = 0;
    while (i < s.size() && isspace((unsigned char)s[i])) i++;
    if (i >= s.size() || s[i] != '"') exit(1);
    i++;
    string val;
    while (i < s.size() && s[i] != '"') val += s[i++];
    if (i >= s.size() || s[i] != '"') exit(1);
    return val;
}

static pair<string, int> parseInput(const string& line) {
    size_t comma = line.rfind(',');
    if (comma == string::npos) exit(1);
    string s = parseQuotedString(line.substr(0, comma));
    size_t i = comma + 1;
    while (i < line.size() && isspace((unsigned char)line[i])) i++;
    int n = stoi(line.substr(i));
    return {s, n};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    if (!getline(cin, line)) return 0;
    while (!line.empty() && isspace((unsigned char)line.back())) line.pop_back();
    auto [s, n] = parseInput(line);
    Solution sol;
    string ans = sol.processChunks(s, n);
    cout << '"' << ans << '"' << '\n';
    return 0;
}
