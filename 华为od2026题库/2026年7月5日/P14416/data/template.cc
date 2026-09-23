#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
using namespace std;

// 找顶层逗号（括号深度 0）
static int findTopLevelComma(const string& s) {
    int bracket = 0;
    bool inString = false;
    for (int i = 0; i < (int)s.size(); i++) {
        char c = s[i];
        if (c == '"') inString = !inString;
        else if (!inString) {
            if (c == '[') bracket++;
            else if (c == ']') bracket--;
            else if (c == ',' && bracket == 0) return i;
        }
    }
    return -1;
}

// 解析 JSON 字符串数组 ["a","b","c"]
static vector<string> parseStringArray(const string& s) {
    vector<string> res;
    int pos = 0;
    bool inStr = false;
    string cur;
    while (pos < (int)s.size()) {
        char c = s[pos];
        if (c == '"') {
            inStr = !inStr;
            if (!inStr) {
                res.push_back(cur);
                cur.clear();
            }
        } else if (inStr) {
            cur += c;
        }
        pos++;
    }
    return res;
}

int main() {
    string line;
    getline(cin, line);

    int comma = findTopLevelComma(line);
    int splitLine = stoi(line.substr(0, comma));

    string rest = line.substr(comma + 1);
    vector<string> sqlText = parseStringArray(rest);

    Solution solution;
    cout << solution.splitSQLToFiles(splitLine, sqlText) << endl;
    return 0;
}
