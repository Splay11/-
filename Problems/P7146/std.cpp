#include <iostream>
#include <string>
#include <vector>
using namespace std;

// 用栈处理括号，线性扫一遍表达式
long long solve(const string& s) {
    vector<long long> stack;
    long long res = 0;
    long long sign = 1;
    int n = (int)s.size();
    int i = 0;
    while (i < n) {
        char c = s[i];
        if (c == ' ') {
            // 空格没有意义，直接跳过
            i++;
            continue;
        }
        if (c >= '0' && c <= '9') {
            // 把连续数字拼成一个整数
            long long num = 0;
            while (i < n && s[i] >= '0' && s[i] <= '9') {
                num = num * 10 + (s[i] - '0');
                i++;
            }
            res += sign * num;
            continue;
        }
        if (c == '+') {
            // 加号只能当二元运算符，下一个项取正
            sign = 1;
            i++;
            continue;
        }
        if (c == '-') {
            // 减号既可二元也可一元，效果都是下一个项取负
            sign = -1;
            i++;
            continue;
        }
        if (c == '(') {
            // 进入新括号层：外层结果和括号前符号先存起来
            stack.push_back(res);
            stack.push_back(sign);
            res = 0;
            sign = 1;
            i++;
            continue;
        }
        // 右括号：用括号前符号把内层结果并回外层
        long long prev_sign = stack.back();
        stack.pop_back();
        long long prev_res = stack.back();
        stack.pop_back();
        res = prev_res + prev_sign * res;
        i++;
    }
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    // 表达式含空格，必须整行读入
    string s;
    getline(cin, s);
    cout << solve(s) << '\n';
    return 0;
}
