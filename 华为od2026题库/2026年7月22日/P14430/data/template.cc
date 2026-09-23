#include "foo.cc"
#include <iostream>
#include <vector>
#include <string>
#include <cctype>
using namespace std;

int main() {
    string line;
    if (!getline(cin, line)) return 0;

    // 提取所有整数（支持可选负号），忽略括号与逗号
    vector<int> arr;
    int num = 0;
    bool have = false;
    bool neg = false;
    for (char c : line) {
        if (isdigit((unsigned char)c)) {
            num = num * 10 + (c - '0');
            have = true;
        } else if (c == '-' && !have) {
            neg = true;
        } else if (have) {
            arr.push_back(neg ? -num : num);
            num = 0; have = false; neg = false;
        }
    }
    if (have) arr.push_back(neg ? -num : num);

    Solution solution;
    cout << solution.countDistinctTags(arr) << endl;
    return 0;
}
