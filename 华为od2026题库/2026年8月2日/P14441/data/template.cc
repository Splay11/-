#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
using namespace std;

// 解析整数列表 [a1,a2,...,an]
static vector<int> parseIntList(const string& s) {
    vector<int> res;
    int i = 0;
    int n = (int)s.size();
    while (i < n && s[i] != '[') i++; // 跳过非括号字符
    i++; // 跳过 [
    int cur = 0;
    bool hasNum = false;
    while (i < n) {
        char c = s[i];
        if (c >= '0' && c <= '9') {
            cur = cur * 10 + (c - '0');
            hasNum = true;
        } else if (c == ',' || c == ']') {
            if (hasNum) {
                res.push_back(cur);
                cur = 0;
                hasNum = false;
            }
            if (c == ']') break;
        }
        i++;
    }
    return res;
}

int main() {
    string line;
    getline(cin, line);

    // 解析 k,m,w,[...]
    int firstComma = line.find(',');
    int k = stoi(line.substr(0, firstComma));

    string rest1 = line.substr(firstComma + 1);
    int secondComma = rest1.find(',');
    int m = stoi(rest1.substr(0, secondComma));

    string rest2 = rest1.substr(secondComma + 1);
    int thirdComma = rest2.find(',');
    int w = stoi(rest2.substr(0, thirdComma));

    string rest3 = rest2.substr(thirdComma + 1);
    vector<int> a = parseIntList(rest3);

    Solution solution;
    cout << solution.minSkillSegments(k, m, w, a) << endl;
    return 0;
}
