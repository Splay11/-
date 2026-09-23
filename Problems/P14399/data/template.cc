#include <algorithm>
#include <cctype>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

#include "foo.cc"

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

static vector<int> parseArray1d(const string& s, size_t start) {
    size_t i = start;
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

static vector<vector<int>> parseArray2d(const string& s, size_t start) {
    size_t i = start;
    while (i < s.size() && isspace((unsigned char)s[i])) i++;
    if (i >= s.size() || s[i] != '[') exit(1);
    i++;
    vector<vector<int>> rows;
    while (true) {
        while (i < s.size() && isspace((unsigned char)s[i])) i++;
        if (i < s.size() && s[i] == ']') {
            i++;
            break;
        }
        if (i >= s.size() || s[i] != '[') exit(1);
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
        rows.push_back(row);
        while (i < s.size() && isspace((unsigned char)s[i])) i++;
        if (i < s.size() && s[i] == ']') {
            i++;
            break;
        }
        if (i >= s.size() || s[i] != ',') exit(1);
        i++;
    }
    return rows;
}

static vector<string> splitTopLevel(const string& line) {
    vector<string> parts;
    size_t start = 0;
    int depth = 0;
    for (size_t i = 0; i < line.size(); i++) {
        if (line[i] == '[') depth++;
        else if (line[i] == ']') depth--;
        else if (line[i] == ',' && depth == 0) {
            parts.push_back(line.substr(start, i - start));
            start = i + 1;
        }
    }
    parts.push_back(line.substr(start));
    return parts;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    if (!getline(cin, line)) return 0;
    while (!line.empty() && isspace((unsigned char)line.back())) line.pop_back();
    auto parts = splitTopLevel(line);
    auto loads = parseArray1d(parts[0], 0);
    auto edges = parseArray2d(parts[1], 0);
    Solution sol;
    cout << sol.maxZoneImbalance(loads, edges) << '\n';
    return 0;
}
