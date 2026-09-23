#include "foo.cc"
#include <bits/stdc++.h>
using namespace std;

static string parseInputString(string s) {
    while (!s.empty() && isspace((unsigned char)s.front())) s.erase(s.begin());
    while (!s.empty() && isspace((unsigned char)s.back())) s.pop_back();
    if (s.size() >= 2 && s.front() == '"' && s.back() == '"') {
        return s.substr(1, s.size() - 2);
    }
    return s;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string line, all;
    while (getline(cin, line)) all += line;

    Solution solution;
    cout << solution.countValidPatterns(parseInputString(all));
    return 0;
}
