#include <iostream>
#include <string>
using namespace std;

// 从 [left,right] 向两边扩张，统计以这里为中心的回文个数
int expand(const string& s, int left, int right) {
    int n = (int)s.size();
    int cnt = 0;
    while (left >= 0 && right < n && s[left] == s[right]) {
        cnt++;
        left--;
        right++;
    }
    return cnt;
}

// 枚举每个中心：奇数中心是一个字符，偶数中心在两个字符之间
int solve(const string& s) {
    int n = (int)s.size();
    int ans = 0;
    for (int i = 0; i < n; i++) {
        // 以 s[i] 为中心的奇数回文
        ans += expand(s, i, i);
        // 以 s[i] 和 s[i+1] 缝为中心的偶数回文
        ans += expand(s, i, i + 1);
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s;
    cin >> s;
    cout << solve(s) << '\n';
    return 0;
}
