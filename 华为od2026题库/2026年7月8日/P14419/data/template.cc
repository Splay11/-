#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
using namespace std;

static vector<int> parseIntList(const string& s) {
    vector<int> res;
    int val = 0, sign = 1;
    bool inNum = false;
    for (char c : s) {
        if (c == '-') { sign = -1; inNum = true; }
        else if (c >= '0' && c <= '9') { val = val * 10 + (c - '0'); inNum = true; }
        else {
            if (inNum) { res.push_back(sign * val); val = 0; sign = 1; inNum = false; }
        }
    }
    return res;
}

static vector<vector<int>> parseInt2DList(const string& s) {
    vector<vector<int>> res;
    const char* p = s.c_str();
    while (*p) {
        if (*p == '[' && (*(p+1) >= '0' && *(p+1) <= '9' || *(p+1) == '-')) {
            p++;
            int a = 0, b = 0, sign = 1;
            bool neg = false;
            if (*p == '-') { neg = true; p++; }
            while (*p >= '0' && *p <= '9') a = a * 10 + (*p++ - '0');
            if (neg) a = -a;
            while (*p < '0' || *p > '9') p++;
            neg = false;
            if (*p == '-') { neg = true; p++; }
            while (*p >= '0' && *p <= '9') b = b * 10 + (*p++ - '0');
            if (neg) b = -b;
            res.push_back({a, b});
            if (*p == ']') p++;
        } else {
            p++;
        }
    }
    return res;
}

int main() {
    string line;
    getline(cin, line);

    // 找顶层逗号
    int depth = 0;
    vector<int> splits;
    for (int i = 0; i < (int)line.size(); i++) {
        if (line[i] == '[') depth++;
        else if (line[i] == ']') depth--;
        else if (line[i] == ',' && depth == 0) splits.push_back(i);
    }

    vector<int> green = parseIntList(line.substr(0, splits[0]));
    vector<int> carbon = parseIntList(line.substr(splits[0] + 1, splits[1] - splits[0] - 1));
    vector<vector<int>> edges = parseInt2DList(line.substr(splits[1] + 1));

    Solution solution;
    cout << solution.maxCarbonReduction(green, carbon, edges) << endl;
    return 0;
}
