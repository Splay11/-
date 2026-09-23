#include "foo.cc"
#include <vector>
#include <string>
#include <iostream>
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

    vector<int> nums = parseIntList(line);

    Solution solution;
    cout << solution.longestNonConsecutiveSubstring(nums) << endl;
    return 0;
}
