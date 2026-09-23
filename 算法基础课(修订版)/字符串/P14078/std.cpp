#include <iostream>
#include <string>

using namespace std;

int main() {
    string A, B;
    cin >> A >> B; // 输入字符串 A 和 B
    
    // 计算 A 和 B 的长度
    int lenA = A.length();
    int lenB = B.length();
    
    // 判断 B 的长度是否是 A 的整数倍
    if (lenB % lenA != 0) {
        cout << "No" << endl; // 如果不是，输出 "No"
        return 0;
    }
    
    // 计算重复的次数
    int k = lenB / lenA;
    string constructed = ""; // 构造字符串
    for (int i = 0; i < k; i++) {
        constructed += A; // 将 A 重复 k 次
    }
    
    // 比较构造的字符串和 B
    if (constructed == B) {
        cout << "Yes" << endl; // 如果相等，输出 "Yes"
    } else {
        cout << "No" << endl; // 否则，输出 "No"
    }
    
    return 0;
}
