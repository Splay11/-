#include <iostream>
#include <string>

using namespace std;

// 检查字符串是否是回文
bool isPalindrome(const string& str) {
    int left = 0, right = str.length() - 1;
    while (left < right) {
        if (str[left] != str[right]) {
            return false; // 如果不相等，返回 false
        }
        left++;
        right--;
    }
    return true; // 全部字符都匹配，返回 true
}

int main() {
    string A, B;
    cin >> A >> B;

    // 在字符串 A 的所有可能插入位置尝试插入 B
    // 包括开头和结尾的情况
    for (int i = 0; i <= A.length(); i++) {
        // 构造新字符串
        string newString = A.substr(0, i) + B + A.substr(i);
        if (isPalindrome(newString)) {
            cout << "YES" << endl;
            return 0; // 找到一个回文，立即返回
        }
    }

    cout << "NO" << endl; // 如果没有找到回文，输出 NO
    return 0;
}
