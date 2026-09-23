#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
using namespace std;

// 在字符串 s 中找到第一个处于括号深度 0 的逗号位置
static int findTopLevelComma(const string& s) {
    int bracket = 0;
    bool inString = false;
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

// 解析 JSON 字符串列表 ["a","b","c"] → vector<string>
static vector<string> parseStringList(const string& s, int& pos) {
    vector<string> res;
    while (pos < (int)s.size() && s[pos] != ']') {
        if (s[pos] == '"') {
            pos++;  // 跳过左引号
            string cur;
            while (pos < (int)s.size() && s[pos] != '"') {
                cur += s[pos];
                pos++;
            }
            res.push_back(cur);
            pos++;  // 跳过右引号
        } else {
            pos++;
        }
    }
    return res;
}

// 解析 JSON 二维字符串数组 → vector<vector<string>>
static vector<vector<string>> parseMatches(const string& s) {
    vector<vector<string>> res;
    int pos = 0;
    while (pos < (int)s.size()) {
        if (s[pos] == '[') {
            pos++;  // 跳过 [
            vector<string> match = parseStringList(s, pos);
            if (!match.empty()) {
                res.push_back(match);
            }
            pos++;  // 跳过 ]
        } else {
            pos++;
        }
    }
    return res;
}

int main() {
    string line;
    getline(cin, line);

    int comma = findTopLevelComma(line);
    int teamNum = stoi(line.substr(0, comma));

    string rest = line.substr(comma + 1);
    vector<vector<string>> matches = parseMatches(rest);

    Solution solution;
    vector<string> result = solution.getTopThree(teamNum, matches);

    // 输出 JSON 数组
    cout << "[";
    for (int i = 0; i < (int)result.size(); i++) {
        if (i > 0) cout << ",";
        cout << '"' << result[i] << '"';
    }
    cout << "]" << endl;

    return 0;
}
