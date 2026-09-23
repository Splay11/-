#include <iostream>
#include <string>
using namespace std;

// 递归函数：反转字符串
string reverseString(const string& s) {
    // 基准条件：如果字符串为空或长度为1，直接返回原字符串
    if (s.length() <= 1) {
        return s;
    }
    // 递归：反转剩余部分，拼接当前字符
    return reverseString(s.substr(1)) + s[0];
}

int main() {
    string s;
    cin >> s;  // 输入字符串
    cout << reverseString(s) << endl;  // 输出反转后的字符串
    return 0;
}
