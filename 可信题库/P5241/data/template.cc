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

static bool parseInt(const string& s, size_t& i, int& out) {
    while (i < s.size() && isspace((unsigned char)s[i])) i++;
    int sign = 1;
    if (i < s.size() && s[i] == '-') {
        sign = -1;
        i++;
    }
    if (i >= s.size() || !isdigit((unsigned char)s[i])) return false;
    long long v = 0;
    while (i < s.size() && isdigit((unsigned char)s[i])) {
        v = v * 10 + (s[i] - '0');
        i++;
    }
    out = (int)(sign * v);
    return true;
}

static vector<int> parseArray1d(const string& line) {
    string s = trim(line);
    size_t i = 0;
    if (i >= s.size() || s[i] != '[') exit(1);
    i++;
    vector<int> row;
    while (true) {
        while (i < s.size() && isspace((unsigned char)s[i])) i++;
        if (i < s.size() && s[i] == ']') {
            i++;
            break;
        }
        int v;
        if (!parseInt(s, i, v)) exit(1);
        row.push_back(v);
        while (i < s.size() && isspace((unsigned char)s[i])) i++;
        if (i < s.size() && s[i] == ']') {
            i++;
            break;
        }
        if (i >= s.size() || s[i] != ',') exit(1);
        i++;
    }
    return row;
}

static string fmtList(const vector<int>& a) {
    if (a.empty()) return "[]";
    string s = "[";
    for (size_t i = 0; i < a.size(); i++) {
        if (i) s += ", ";
        s += to_string(a[i]);
    }
    s += "]";
    return s;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line1, line2, line3;
    if (!getline(cin, line1)) return 0;
    if (!getline(cin, line2)) return 0;
    if (!getline(cin, line3)) return 0;
    auto arrival = parseArray1d(line1);
    auto duration = parseArray1d(line2);
    auto priority = parseArray1d(line3);
    Solution sol;
    cout << fmtList(sol.finishTimes(arrival, duration, priority)) << '\n';
    return 0;
}
