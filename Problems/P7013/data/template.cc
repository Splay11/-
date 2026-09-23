#include "foo.cc"
#include <cctype>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

static string trim(const string& s) {
    size_t a = 0; while (a < s.size() && isspace((unsigned char)s[a])) a++;
    size_t b = s.size(); while (b > a && isspace((unsigned char)s[b - 1])) b--;
    return s.substr(a, b - a);
}
static bool parseLong(const string& s, size_t& i, long long& out) {
    while (i < s.size() && isspace((unsigned char)s[i])) i++;
    int sign = 1; if (i < s.size() && s[i] == '-') { sign = -1; i++; }
    if (i >= s.size() || !isdigit((unsigned char)s[i])) return false;
    long long v = 0; while (i < s.size() && isdigit((unsigned char)s[i])) { v = v * 10 + (s[i] - '0'); i++; }
    out = sign * v; return true;
}
static vector<int> parseArray1d(const string& line) {
    string s = trim(line); size_t i = 0;
    if (i >= s.size() || s[i] != '[') exit(1); i++;
    vector<int> row;
    while (true) {
        while (i < s.size() && isspace((unsigned char)s[i])) i++;
        if (i < s.size() && s[i] == ']') { i++; break; }
        long long v; if (!parseLong(s, i, v)) exit(1); row.push_back((int)v);
        while (i < s.size() && isspace((unsigned char)s[i])) i++;
        if (i < s.size() && s[i] == ']') { i++; break; }
        if (i >= s.size() || s[i] != ',') exit(1); i++;
    }
    return row;
}

int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    string l1, l2; if (!getline(cin, l1) || !getline(cin, l2)) return 0;
    auto versions = parseArray1d(l1); Solution sol;
    cout << sol.countNeedUpgrade(versions, stoi(trim(l2))) << '\n';
}
