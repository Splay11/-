#include <bits/stdc++.h>
using namespace std;

// 对串做一次从左到右的平衡字母变换
string apply_once(string s) {
    int n = (int)s.size();
    array<int, 26> freq{}, left{};
    for (char ch : s) ++freq[ch - 'a'];
    for (int i = 0; i < n; ++i) {
        int c = s[i] - 'a';
        if (left[c] == freq[c] - left[c] - 1) {
            --freq[c];
            int nc = (c + 1) % 26;
            s[i] = char('a' + nc);
            ++freq[nc];
            ++left[nc];
        } else ++left[c];
    }
    return s;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    while (q--) {
        int m, r;
        string z;
        cin >> m >> r >> z;
        deque<string> window;
        window.push_back(z);
        int done = 0;
        while (done < r) {
            string nxt = apply_once(z);
            ++done;
            if (nxt == z) break; // 已稳定
            z.swap(nxt);
            window.push_back(z);
            if ((int)window.size() > 27) window.pop_front();
            if ((int)window.size() == 27 && window.front() == window.back()) {
                // 周期 26：跳转剩余变换
                int rem = r - done;
                string s0 = window[0], s1 = window[1];
                int add = rem % 26;
                for (int i = 0; i < m; ++i)
                    if (s0[i] != s1[i])
                        z[i] = char('a' + (z[i] - 'a' + add) % 26);
                break;
            }
        }
        cout << z << '\n';
    }
    return 0;
}
