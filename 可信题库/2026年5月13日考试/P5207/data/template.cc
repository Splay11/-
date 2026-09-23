#include "foo.cc"
#include <iostream>
#include <string>

using namespace std;

static string parseQuoted(const string& line) {
    if (line.size() >= 2 && line.front() == '"' && line.back() == '"')
        return line.substr(1, line.size() - 2);
    return line;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    if (!getline(cin, line)) return 0;
    Solution sol;
    string ans = sol.flipWorkId(parseQuoted(line));
    cout << "\"" << ans << "\"\n";
    return 0;
}
