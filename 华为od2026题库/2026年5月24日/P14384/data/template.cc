#include "foo.cc"
#include <cctype>
#include <iostream>
#include <string>
#include <tuple>
#include <vector>

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
        v = v * 10 + (s[i] - '0');
        i++;
    }
    if (!ok) exit(1);
    return sign * v;
}

static vector<vector<int>> parseCars(const string& s, size_t start) {
    vector<vector<int>> out;
    size_t i = start;
    while (i < s.size() && isspace((unsigned char)s[i])) i++;
    if (i >= s.size() || s[i] != '[') exit(1);
    i++;
    while (true) {
        while (i < s.size() && isspace((unsigned char)s[i])) i++;
        if (i < s.size() && s[i] == ']') {
            i++;
            break;
        }
        if (s[i] != '[') exit(1);
        i++;
        vector<int> row;
        while (true) {
            while (i < s.size() && isspace((unsigned char)s[i])) i++;
            if (i < s.size() && s[i] == ']') {
                i++;
                break;
            }
            row.push_back(readInt(s, i));
            while (i < s.size() && isspace((unsigned char)s[i])) i++;
            if (i < s.size() && s[i] == ']') {
                i++;
                break;
            }
            if (i >= s.size() || s[i] != ',') exit(1);
            i++;
        }
        out.push_back(row);
        while (i < s.size() && isspace((unsigned char)s[i])) i++;
        if (i < s.size() && s[i] == ']') {
            i++;
            break;
        }
        if (i >= s.size() || s[i] != ',') exit(1);
        i++;
    }
    return out;
}

static tuple<int, int, vector<vector<int>>> parseLine(const string& line) {
    size_t i = 0;
    int n = readInt(line, i);
    if (i >= line.size() || line[i] != ',') exit(1);
    i++;
    int m = readInt(line, i);
    if (i >= line.size() || line[i] != ',') exit(1);
    i++;
    auto cars = parseCars(line, i);
    return {n, m, cars};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    if (!getline(cin, line)) return 0;
    auto pk = parseLine(line);
    Solution sol;
    cout << sol.countFailedCharging(get<0>(pk), get<2>(pk)) << "\n";
    return 0;
}
