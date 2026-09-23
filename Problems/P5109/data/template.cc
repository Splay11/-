#include "foo.cc"
#include <iostream>
#include <string>
#include <vector>

using namespace std;

static vector<string> parseTwoQuotedStrings(const string& line) {
    vector<string> res;
    size_t i = 0;
    for (int k = 0; k < 2; k++) {
        while (i < line.size() && line[i] != '"') i++;
        if (i >= line.size()) exit(1);
        i++;
        size_t start = i;
        while (i < line.size() && line[i] != '"') i++;
        res.push_back(line.substr(start, i - start));
        if (i < line.size() && line[i] == '"') i++;
        if (k == 0 && i < line.size() && line[i] == ',') i++;
    }
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    if (!getline(cin, line)) return 0;
    while (!line.empty() && (line.back() == '\r' || line.back() == '\n')) line.pop_back();
    auto parts = parseTwoQuotedStrings(line);
    Solution sol;
    int ans = sol.minDistinctAfterSwap(parts[0], parts[1]);
    cout << ans << '\n';
    return 0;
}
