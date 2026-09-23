#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
using namespace std;

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

// 解析以 " 包裹的字符串，返回引号内的内容
static string parseQuotedString(const string& s) {
    size_t start = s.find('"');
    size_t end = s.rfind('"');
    if (start == string::npos || end == string::npos || start >= end)
        return "";
    return s.substr(start + 1, end - start - 1);
}

// 解析整型数组 [a,b,c,...]
static vector<int> parseIntList(const string& s) {
    vector<int> res;
    int n = (int)s.size();
    int num = 0;
    bool hasNum = false;
    for (int i = 0; i < n; i++) {
        char c = s[i];
        if (c >= '0' && c <= '9') {
            num = num * 10 + (c - '0');
            hasNum = true;
        } else if ((c == ',' || c == ']') && hasNum) {
            res.push_back(num);
            num = 0;
            hasNum = false;
            if (c == ']') break;
        }
    }
    return res;
}

int main() {
    string line;
    getline(cin, line);

    // 找到第一个顶层逗号（CIDR 之后）
    int comma1 = findTopLevelComma(line);
    string cidrPart = line.substr(0, comma1);
    string cidr = parseQuotedString(cidrPart);

    // 找到第二个顶层逗号（N 之后）
    string rest = line.substr(comma1 + 1);
    int comma2 = findTopLevelComma(rest);
    int n = stoi(rest.substr(0, comma2));

    // 剩余部分是需求数组
    string reqStr = rest.substr(comma2 + 1);
    vector<int> requirements = parseIntList(reqStr);

    Solution solution;
    vector<string> result = solution.allocateSubnets(cidr, n, requirements);

    // 输出结果
    cout << "[";
    for (int i = 0; i < (int)result.size(); i++) {
        if (i > 0) cout << ",";
        cout << "\"" << result[i] << "\"";
    }
    cout << "]" << endl;

    return 0;
}
