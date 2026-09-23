#include "foo.cc"
#include <cctype>
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <climits>
using namespace std;

static int readInt(const string& s, size_t& i) {
    while (i < s.size() && isspace((unsigned char)s[i])) i++;
    int sign = 1;
    if (i < s.size() && s[i] == '-') {
        sign = -1;
        i++;
    }
    int v = 0;
    bool ok = false;
    while (i < s.size() && isdigit((unsigned char)s[i])) {
        ok = true;
        v = v * 10 + (s[i++] - '0');
    }
    if (!ok) exit(1);
    return sign * v;
}

static vector<int> parseArray1d(const string& s, size_t start) {
    size_t i = start;
    if (i >= s.size() || s[i] != '[') exit(1);
    i++;
    vector<int> vals;
    while (true) {
        while (i < s.size() && isspace((unsigned char)s[i])) i++;
        if (i < s.size() && s[i] == ']') {
            i++;
            break;
        }
        vals.push_back(readInt(s, i));
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
    size_t p = line.find('[');
    if (p == string::npos) return 1;
    size_t i = 0;
    int n = readInt(line, i);
    if (i >= p || line[i] != ',') return 1;
    i++;
    int m = readInt(line, i);
    if (i >= p || line[i] != ',') return 1;
    i++;
    int k = readInt(line, i);
    auto demands = parseArray1d(line, p);
    Solution sol;
    cout << sol.maxChargingDemand(n, m, k, demands) << "\n";
    return 0;
}
