#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
using namespace std;

// 解析形如 [1,2,3] 的整数数组
static vector<int> parseArray(const string& s) {
    vector<int> res;
    string cur;
    for (char c : s) {
        if (c >= '0' && c <= '9') {
            cur += c;
        } else if (c == ',' || c == ']') {
            if (!cur.empty()) {
                res.push_back(stoi(cur));
                cur.clear();
            }
        }
    }
    return res;
}

int main() {
    string line;
    getline(cin, line);
    vector<int> nums = parseArray(line);
    Solution solution;
    cout << solution.longestSubarray(nums) << endl;
    return 0;
}
