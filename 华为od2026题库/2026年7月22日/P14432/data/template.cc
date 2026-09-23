#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
using namespace std;

// 找到括号深度为 0 的第一个逗号（用于切分顶层字段 n,m,files,cost）
static int findTopLevelComma(const string& s) {
    int bracket = 0;
    for (int i = 0; i < (int)s.size(); i++) {
        char c = s[i];
        if (c == '[') bracket++;
        else if (c == ']') bracket--;
        else if (c == ',' && bracket == 0) return i;
    }
    return -1;
}

// 解析一维整数列表，如 [1,2,2]
static void parseIntVector(const string& s, vector<int>& out) {
    int i = 0, n = (int)s.size();
    while (i < n && s[i] != '[') i++;
    i++;  // 跳过 '['
    string cur;
    while (i < n) {
        char c = s[i];
        if (c >= '0' && c <= '9') {
            cur += c;
        } else if (c == ',' || c == ']') {
            // 遇到逗号或 ']' 时结算当前整数
            if (!cur.empty()) {
                out.push_back(stoi(cur));
                cur.clear();
            }
            if (c == ']') break;  // 列表结束
        }
        i++;
    }
}

// 解析二维整数列表，如 [[0,1],[1,2],[0,2]]
static void parseIntMatrix(const string& s, vector<vector<int>>& out) {
    int i = 0, n = (int)s.size();
    while (i < n && s[i] != '[') i++;
    i++;  // 跳过外层 '['
    while (i < n && s[i] != ']') {
        if (s[i] == '[') {
            // 找到本行匹配的 ']'，提取子串后复用一维解析
            int depth = 0, j = i;
            for (; j < n; j++) {
                if (s[j] == '[') depth++;
                else if (s[j] == ']') {
                    depth--;
                    if (depth == 0) break;
                }
            }
            vector<int> row;
            parseIntVector(s.substr(i, j - i + 1), row);
            out.push_back(row);
            i = j + 1;
            while (i < n && (s[i] == ',' || s[i] == ' ')) i++;
        } else {
            i++;
        }
    }
}

int main() {
    string line;
    getline(cin, line);

    // 依次按顶层逗号切分为 n, m, files, cost 四段
    int c1 = findTopLevelComma(line);
    int n = stoi(line.substr(0, c1));
    string rest1 = line.substr(c1 + 1);

    int c2 = findTopLevelComma(rest1);
    int m = stoi(rest1.substr(0, c2));
    string rest2 = rest1.substr(c2 + 1);

    int c3 = findTopLevelComma(rest2);
    string filesStr = rest2.substr(0, c3);
    string costStr = rest2.substr(c3 + 1);

    vector<vector<int>> files;
    parseIntMatrix(filesStr, files);
    vector<int> cost;
    parseIntVector(costStr, cost);

    Solution solution;
    cout << solution.minCost(n, m, files, cost) << endl;
    return 0;
}
