#include <iostream>
#include <string>
#include <vector>
using namespace std;

bool canQueue(const string& u, const string& v) {
    return u == v;
}

bool canStack(const string& u, const string& v) {
    vector<char> st;
    int i = 0;
    int n = (int)u.size();
    // 按出站序列贪心：栈顶不匹配就继续入站
    for (char c : v) {
        while (i < n && (st.empty() || st.back() != c)) {
            st.push_back(u[i]);
            ++i;
        }
        if (st.empty() || st.back() != c) {
            return false;
        }
        st.pop_back();
    }
    return true;
}

string solve(const string& u, const string& v) {
    bool q = canQueue(u, v);
    bool s = canStack(u, v);
    if (q && s) return "both";
    if (q) return "queue";
    if (s) return "stack";
    return "neither";
}

int main() {
    string u, v;
    cin >> u >> v;
    cout << solve(u, v) << endl;
    return 0;
}
