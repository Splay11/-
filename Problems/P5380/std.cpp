#include <iostream>
#include <string>
#include <vector>
using namespace std;

// 用栈做最近未匹配开启桩配对，统计内部长度能被 m 整除的舱段数
long long count_cabin(int n, int m, const string &t) {
    // 栈里存尚未配对的 '(' 下标（从 0 起）
    vector<int> st;
    long long ans = 0;
    for (int i = 0; i < n; i++) {
        if (t[i] == '(') {
            // 开启桩入栈，等待之后最近的闭合桩来配对
            st.push_back(i);
        } else {
            // 闭合桩与栈顶（左侧最近未匹配开启桩）配对
            int left = st.back();
            st.pop_back();
            // 内部长度 = 两端下标差再减 1，即中间桩标个数
            int inner = i - left - 1;
            if (inner % m == 0) {
                ans++;
            }
        }
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    string t;
    cin >> n >> m;
    cin >> t;
    cout << count_cabin(n, m, t) << "\n";
    return 0;
}
