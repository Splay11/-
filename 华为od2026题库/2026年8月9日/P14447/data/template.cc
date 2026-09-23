#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
using namespace std;

// 解析整型列表 "[a,b,c,...]"
static vector<int> parseIntList(const string& s) {
    vector<int> res;
    int i = 1;  // 跳过开头的 '['
    int n = (int)s.size();
    while (i < n) {
        // 跳过空格
        while (i < n && (s[i] == ' ')) i++;
        if (i >= n || s[i] == ']') break;
        int sign = 1;
        if (s[i] == '-') { sign = -1; i++; }
        int num = 0;
        while (i < n && s[i] >= '0' && s[i] <= '9') {
            num = num * 10 + (s[i] - '0');
            i++;
        }
        res.push_back(sign * num);
        // 跳过逗号
        if (i < n && s[i] == ',') i++;
    }
    return res;
}

// 找到顶层逗号（不在括号内的逗号）
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

int main() {
    string line;
    getline(cin, line);

    // 解析 count
    int comma1 = findTopLevelComma(line);
    int count = stoi(line.substr(0, comma1));

    // 解析 total
    string rest1 = line.substr(comma1 + 1);
    int comma2 = findTopLevelComma(rest1);
    int total = stoi(rest1.substr(0, comma2));

    // 解析数组部分
    string rest2 = rest1.substr(comma2 + 1);
    int split = (int)rest2.find("],[");
    string valuesStr = rest2.substr(0, split + 1);
    string decaysStr = string("[") + rest2.substr(split + 3);

    vector<int> values = parseIntList(valuesStr);
    vector<int> decays = parseIntList(decaysStr);

    Solution solution;
    cout << solution.maxMushroomValue(count, total, values, decays) << endl;
    return 0;
}
