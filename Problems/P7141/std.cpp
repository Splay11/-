#include <iostream>
#include <string>
using namespace std;

// 对每个字母记下第一次和最后一次出现的下标
// 若某字母至少出现两次，中间长度为 last-first-1（不含两端）
int solve(const string& s) {
    int first[26];
    int last[26];
    for (int i = 0; i < 26; i++) {
        first[i] = -1;
        last[i] = -1;
    }
    for (int i = 0; i < (int)s.size(); i++) {
        int id = s[i] - 'a';
        if (first[id] == -1) {
            first[id] = i;
        }
        last[id] = i;
    }
    int ans = -1;
    for (int c = 0; c < 26; c++) {
        if (first[c] != -1 && last[c] > first[c]) {
            // 只统计出现至少两次的字母
            int length = last[c] - first[c] - 1;
            if (length > ans) {
                ans = length;
            }
        }
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
