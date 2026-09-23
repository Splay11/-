#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n; // 读入正整数 n
    int count = 0; // 初始化满足条件的整数计数

    for (int i = 1; i <= n; ++i) {
        int sum_of_digits = 0; // 存储当前数字 i 各位数字之和
        int num = i; // 复制 i，用于提取各位数字

        // 计算各位数字之和
        while (num > 0) {
            sum_of_digits += num % 10; // 取末尾数字并累加
            num /= 10; // 去掉末尾数字
        }

        // 计算末尾数字 d(i)
        int last_digit = i % 10;

        // 检查条件 S(i) mod 10 = d(i)
        if (sum_of_digits % 10 == last_digit) {
            count++; // 满足条件，计数加一
        }
    }

    cout << count << endl; // 输出结果
    return 0;
}
