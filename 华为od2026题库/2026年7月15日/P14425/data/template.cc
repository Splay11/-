#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
using namespace std;

// 解析形如 ["a","b","c"] 的字符串数组（提取所有引号内的内容）
static vector<string> parseStringList(const string& s) {
    vector<string> res;
    string cur;
    bool inString = false;
    for (char c : s) {
        if (c == '"') {
            if (inString) {
                res.push_back(cur);
                cur.clear();
            }
            inString = !inString;
        } else if (inString) {
            cur += c;
        }
    }
    return res;
}

int main() {
    string line;
    getline(cin, line);

    // 整行即 JSON 字符串数组，提取所有字符串
    vector<string> dates = parseStringList(line);

    Solution solution;
    vector<string> ans = solution.normalizeDates(dates);

    // 按题面格式输出：["a","b",...]（无空格）
    cout << '[';
    for (size_t i = 0; i < ans.size(); i++) {
        if (i) cout << ',';
        cout << '"' << ans[i] << '"';
    }
    cout << ']' << endl;
    return 0;
}
