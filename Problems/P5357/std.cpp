#include <iostream>
#include <string>
#include <vector>
using namespace std;

bool is_valid(const string& t) {
    // 栈里只放还没配上的开封口；遇闭封口必须立刻配栈顶
    vector<char> st;
    for (int i = 0; i < (int)t.size(); i++) {
        char ch = t[i];
        if (ch == '(' || ch == '[' || ch == '{') {
            // 开封口：入栈等待
            st.push_back(ch);
        } else {
            // 闭封口：必须和栈顶同一种
            if (st.empty()) {
                return false;
            }
            char top = st.back();
            if ((ch == ')' && top != '(') || (ch == ']' && top != '[') || (ch == '}' && top != '{')) {
                return false;
            }
            st.pop_back();
        }
    }
    // 还有没扣上的开封口则不合格
    return st.empty();
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    string t;
    // 空文件时 getline 得到空串，按合法处理
    getline(cin, t);
    if (is_valid(t)) {
        cout << "true" << endl;
    } else {
        cout << "false" << endl;
    }
    return 0;
}
