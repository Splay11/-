#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
#include <cctype>
using namespace std;

// 从字符串中提取所有整数（忽略非数字字符，如逗号、括号）
static vector<int> extractInts(const string& s) {
    vector<int> res;
    int cur = 0;
    bool have = false;
    for (char c : s) {
        if (isdigit((unsigned char)c)) {
            cur = cur * 10 + (c - '0');
            have = true;
        } else if (have) {
            res.push_back(cur);
            cur = 0;
            have = false;
        }
    }
    if (have) res.push_back(cur);
    return res;
}

int main() {
    string line;
    if (!getline(cin, line)) return 0;

    // 提取全部整数：前 3 个为 n, m, w，其余每 3 个为一条路线
    vector<int> a = extractInts(line);
    int n = a[0], m = a[1], w = a[2];
    vector<vector<int>> roads;
    for (size_t i = 3; i + 2 < a.size(); i += 3)
        roads.push_back({a[i], a[i + 1], a[i + 2]});

    Solution sol;
    int ans = sol.minCost(n, m, w, roads);
    cout << ans << endl;
    return 0;
}
