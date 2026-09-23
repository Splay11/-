#include <bits/stdc++.h>
using namespace std;

string process(const string& s) {
    // 先去掉所有 b
    string buf;
    for (char ch : s) {
        if (ch != 'b') {
            buf.push_back(ch);
        }
    }
    // 再用栈消除连续的 ac（可反复相邻形成）
    string st;
    for (char ch : buf) {
        if (!st.empty() && st.back() == 'a' && ch == 'c') {
            st.pop_back();
        } else {
            st.push_back(ch);
        }
    }
    return st;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s;
    getline(cin, s);
    cout << process(s) << "\n";
    return 0;
}
