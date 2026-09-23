#include "foo.cc"
#include <cctype>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

static vector<int> parseArray1d(const string& s) {
    size_t i = 0;
    while (i < s.size() && isspace((unsigned char)s[i])) i++;
    if (i >= s.size() || s[i] != '[') exit(1);
    i++;
    vector<int> vals;
    while (true) {
        while (i < s.size() && isspace((unsigned char)s[i])) i++;
        if (i < s.size() && s[i] == ']') {
            i++;
            break;
        }
        int sign = 1;
        if (i < s.size() && s[i] == '-') {
            sign = -1;
            i++;
        }
        int v = 0;
        bool ok = false;
        while (i < s.size() && isdigit((unsigned char)s[i])) {
            ok = true;
            v = v * 10 + (s[i] - '0');
            i++;
        }
        if (!ok) exit(1);
        vals.push_back(sign * v);
        while (i < s.size() && isspace((unsigned char)s[i])) i++;
        if (i < s.size() && s[i] == ']') {
            i++;
            break;
        }
        if (i >= s.size() || s[i] != ',') exit(1);
        i++;
    }
    return vals;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    if (!getline(cin, line)) return 0;
    auto type = parseArray1d(line);
    Solution sol;
    cout << sol.longestValidSkillChain(type) << "\n";
    return 0;
}
