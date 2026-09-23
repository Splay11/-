#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
using namespace std;

// 解析整数数组 "[a1,a2,...,an]"
static vector<int> parseIntList(const string& s) {
    vector<int> res;
    int cur = 0;
    bool neg = false, hasNum = false;
    for (char c : s) {
        if (c == '-') { neg = true; }
        else if (c >= '0' && c <= '9') { cur = cur * 10 + (c - '0'); hasNum = true; }
        else if (c == ',' || c == ']') {
            if (hasNum) { res.push_back(neg ? -cur : cur); cur = 0; neg = false; hasNum = false; }
        }
    }
    return res;
}

int main() {
    string line;
    getline(cin, line);

    // 找到顶层逗号，分割数组和 target
    int bracket = 0, comma = -1;
    for (int i = 0; i < (int)line.size(); ++i) {
        if (line[i] == '[') bracket++;
        else if (line[i] == ']') bracket--;
        else if (line[i] == ',' && bracket == 0) { comma = i; break; }
    }

    vector<int> nums = parseIntList(line.substr(0, comma));
    int target = stoi(line.substr(comma + 1));

    Solution solution;
    vector<vector<int>> result = solution.threeSumWithParity(nums, target);

    // 输出格式：[[a,b,c],[d,e,f]]
    cout << "[";
    for (int i = 0; i < (int)result.size(); ++i) {
        if (i > 0) cout << ",";
        cout << "[";
        for (int j = 0; j < (int)result[i].size(); ++j) {
            if (j > 0) cout << ",";
            cout << result[i][j];
        }
        cout << "]";
    }
    cout << "]" << endl;
    return 0;
}
