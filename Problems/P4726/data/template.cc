#include "foo.cc"
#include <cctype>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

static string trim(const string& s) {
    size_t a = 0;
    while (a < s.size() && isspace((unsigned char)s[a])) a++;
    size_t b = s.size();
    while (b > a && isspace((unsigned char)s[b - 1])) b--;
    return s.substr(a, b - a);
}

static bool splitGridAndK(const string& line, string& gridStr, int& k) {
    string s = trim(line);
    int d = 0;
    int end = -1;
    for (size_t i = 0; i < s.size(); i++) {
        char c = s[i];
        if (c == '[')
            d++;
        else if (c == ']') {
            d--;
            if (d == 0) {
                end = (int)i;
                break;
            }
        }
    }
    if (end < 0) return false;
    gridStr = s.substr(0, (size_t)end + 1);
    string tail = trim(s.substr((size_t)end + 1));
    if (tail.empty() || tail[0] != ',') return false;
    tail = trim(tail.substr(1));
    try {
        k = stoi(tail);
    } catch (...) {
        return false;
    }
    return true;
}

static bool parseGrid2d(const string& s, vector<vector<int>>& out) {
    out.clear();
    size_t i = 0;
    while (i < s.size() && isspace((unsigned char)s[i])) i++;
    if (i >= s.size() || s[i] != '[') return false;
    i++;
    while (true) {
        while (i < s.size() && isspace((unsigned char)s[i])) i++;
        if (i < s.size() && s[i] == ']') {
            i++;
            break;
        }
        if (i >= s.size() || s[i] != '[') return false;
        i++;
        vector<int> row;
        while (true) {
            while (i < s.size() && isspace((unsigned char)s[i])) i++;
            int sign = 1;
            if (i < s.size() && s[i] == '-') {
                sign = -1;
                i++;
            }
            long long v = 0;
            bool ok = false;
            while (i < s.size() && isdigit((unsigned char)s[i])) {
                ok = true;
                v = v * 10 + (s[i] - '0');
                i++;
            }
            if (!ok) return false;
            row.push_back((int)(sign * v));
            while (i < s.size() && isspace((unsigned char)s[i])) i++;
            if (i < s.size() && s[i] == ']') {
                i++;
                break;
            }
            if (i >= s.size() || s[i] != ',') return false;
            i++;
        }
        out.push_back(move(row));
        while (i < s.size() && isspace((unsigned char)s[i])) i++;
        if (i < s.size() && s[i] == ']') {
            i++;
            break;
        }
        if (i >= s.size() || s[i] != ',') return false;
        i++;
    }
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    if (!getline(cin, line)) return 0;
    string gridStr;
    int maxDiff = 0;
    if (!splitGridAndK(line, gridStr, maxDiff)) return 1;
    vector<vector<int>> grid;
    if (!parseGrid2d(gridStr, grid)) return 1;
    Solution sol;
    long long ans = sol.countHikingPaths(grid, maxDiff);
    cout << ans << "\n";
    return 0;
}
