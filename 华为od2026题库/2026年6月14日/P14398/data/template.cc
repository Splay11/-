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

static void printAns(const vector<string>& ans) {
    cout << "[";
    for (size_t i = 0; i < ans.size(); i++) {
        if (i) cout << ",";
        cout << '"' << ans[i] << '"';
    }
    cout << "]\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string line;
    if (!getline(cin, line)) return 0;
    while (!line.empty() && isspace((unsigned char)line.back())) line.pop_back();
    auto parts = splitTopLevel(line);
    auto nums = parseArray1d(parts[0], 0);
    size_t bi = 0;
    int base = readInt(parts[1], bi);
    Solution sol;
    printAns(sol.sortConvertedNums(nums, base));
    return 0;
}
