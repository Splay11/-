#include <iostream>
#include <string>
using namespace std;

// 滑动窗口：对每个右端点，无重复窗口内长度为 k 及以上的子串个数可 O(1) 计算
long long count_unique(const string& s, int k) {
    int n = (int)s.size();
    // last[c]：字符 c 上一次出现的下标，-1 表示还没出现过
    int last[26];
    for (int i = 0; i < 26; i++) {
        last[i] = -1;
    }
    int left = 0;
    long long ans = 0;
    for (int right = 0; right < n; right++) {
        int idx = s[right] - 'a';
        // 窗口内出现重复，把左端推到上一次该字符的右边
        if (last[idx] >= left) {
            left = last[idx] + 1;
        }
        last[idx] = right;
        // 以 right 为右端、长度 >= k 的起点最多到 right-k+1，且不能小于 left
        int limit = right - k + 1;
        if (limit >= left) {
            ans += (long long)(limit - left + 1);
        }
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s;
    int k;
    cin >> s >> k;
    cout << count_unique(s, k) << "\n";
    return 0;
}
