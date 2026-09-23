#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
using namespace std;

// 解析形如 [1,5,3] 的整数列表（忽略括号、空格，按逗号切分）
static vector<int> parseIntList(const string& s) {
    vector<int> res;
    string cur;
    for (char c : s) {
        if (c == '[' || c == ']' || c == ' ') continue;
        if (c == ',') {
            if (!cur.empty()) { res.push_back(stoi(cur)); cur.clear(); }
        } else {
            cur += c;
        }
    }
    if (!cur.empty()) res.push_back(stoi(cur));
    return res;
}

int main() {
    string line;
    getline(cin, line);

    // 顶层逗号：分隔 N 与已交卷列表（N 为纯整数，首个逗号即分隔符）
    int comma = (int)line.find(',');
    int n = stoi(line.substr(0, comma));
    string rest = line.substr(comma + 1);

    vector<int> submitted = parseIntList(rest);

    Solution solution;
    vector<int> ans = solution.findMissingStudents(n, submitted);

    // 按题面格式输出：[a,b,c]（无空格）
    cout << '[';
    for (size_t i = 0; i < ans.size(); i++) {
        if (i) cout << ',';
        cout << ans[i];
    }
    cout << ']' << endl;
    return 0;
}
