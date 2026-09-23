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

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    if (!getline(cin, line)) return 0;
    while (!line.empty() && isspace((unsigned char)line.back())) line.pop_back();
    string s = parseQuotedString(line);
    Solution sol;
    string ans = sol.processString(s);
    cout << '"' << ans << '"' << '\n';
    return 0;
}
