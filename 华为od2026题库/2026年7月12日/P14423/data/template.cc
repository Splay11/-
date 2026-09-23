#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
using namespace std;

// 解析字符串数组 ["a:v1:","b:v1:"] -> vector<string>
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

// 找到两个顶层数组之间的逗号（括号深度为 0 且不在字符串内）
static int findTopLevelComma(const string& s) {
    bool inString = false;
    int bracket = 0;
    for (int i = 0; i < (int)s.size(); i++) {
        char c = s[i];
        if (c == '"') {
            inString = !inString;
        } else if (!inString) {
            if (c == '[') bracket++;
            else if (c == ']') bracket--;
            else if (c == ',' && bracket == 0) return i;
        }
    }
    return -1;
}

int main() {
    string line;
    getline(cin, line);

    int comma = findTopLevelComma(line);
    vector<string> directDeps = parseStringList(line.substr(0, comma));
    vector<string> depRules = parseStringList(line.substr(comma + 1));

    Solution solution;
    vector<string> result = solution.getDependencyOrder(directDeps, depRules);

    // 按题面样例格式输出：["name:version",...]（无空格）
    cout << '[';
    for (size_t i = 0; i < result.size(); i++) {
        if (i) cout << ',';
        cout << '"' << result[i] << '"';
    }
    cout << ']' << endl;
    return 0;
}
