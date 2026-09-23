#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
using namespace std;

static vector<vector<int>> parseTriples(const string& s) {
    vector<vector<int>> res;
    int i = 0, n = (int)s.size();
    while (i < n && s[i] != '[') i++;
    if (i < n) i++;
    while (i < n) {
        while (i < n && (s[i] == ' ' || s[i] == ',')) i++;
        if (i >= n || s[i] == ']') break;
        if (s[i] != '[') { ++i; continue; }
        ++i;
        int vals[3] = {0, 0, 0}, k = 0;
        while (i < n && s[i] != ']' && k < 3) {
            while (i < n && (s[i] == ' ' || s[i] == ',')) i++;
            if (i >= n || s[i] == ']') break;
            int sign = 1;
            if (s[i] == '-') { sign = -1; ++i; }
            long long v = 0;
            while (i < n && s[i] >= '0' && s[i] <= '9') {
                v = v * 10 + (s[i] - '0');
                ++i;
            }
            vals[k++] = (int)(sign * v);
        }
        while (i < n && s[i] != ']') i++;
        if (i < n && s[i] == ']') i++;
        res.push_back({vals[0], vals[1], vals[2]});
    }
    return res;
}

static string readAll() {
    string s, line;
    bool first = true;
    while (getline(cin, line)) {
        if (!first) s.push_back('\n');
        first = false;
        s += line;
    }
    return s;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string raw = readAll();
    string line1, line2;
    auto pos = raw.find('\n');
    if (pos == string::npos) { line1 = raw; line2 = "[]"; }
    else { line1 = raw.substr(0, pos); line2 = raw.substr(pos + 1); }
    int n = 0;
    for (char c : line1) if (c >= '0' && c <= '9') n = n * 10 + (c - '0');
    vector<vector<int>> ops = parseTriples(line2);
    Solution solution;
    cout << solution.maxLinkLoad(n, ops) << endl;
    return 0;
}
