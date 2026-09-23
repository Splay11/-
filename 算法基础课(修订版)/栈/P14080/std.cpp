#include <iostream>
#include <stack>
#include <string>

using namespace std;

int main() {
    string s;
    cin >> s;  // 输入括号字符串
    stack<char> stk;  // 创建一个栈

    for (char ch : s) {
        if (ch == '(') {
            stk.push(ch);  // 遇到左括号，压入栈中
        } else {
            if (stk.empty()) {
                cout << "No" << endl;  // 栈为空，说明没有匹配的左括号
                return 0;
            }
            stk.pop();  // 弹出栈顶元素，匹配对应的左括号
        }
    }

    // 如果栈为空，说明所有左括号都有匹配
    cout << (stk.empty() ? "Yes" : "No") << endl;  // 输出结果

    return 0;
}
