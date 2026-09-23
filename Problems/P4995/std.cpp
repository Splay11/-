#include <bits/stdc++.h>
using namespace std;

string apply_once(string s) {
    int n = (int)s.size();
    array<int, 26> freq{}, left{};
    for (char ch : s) ++freq[ch - 'a'];
    for (int i = 0; i < n; ++i) {
        int c = s[i] - 'a';
        int x = left[c];
        int y = freq[c] - left[c] - 1;
        if (x == y) {
            --freq[c];
            int nc = (c + 1) % 26;
            s[i] = char('a' + nc);
            ++freq[nc];
            ++left[nc];
        } else {
            ++left[c];
        }
    }
    return s;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    if (!(cin >> q)) return 0;
    while (q--) {
        int m, r;
        string z;
        cin >> m >> r >> z;
        deque<string> window;
        window.push_back(z);
        int done = 0;
        bool finished = false;
        while (done < r) {
            string nxt = apply_once(z);
            ++done;
            if (nxt == z) {
                finished = true;
                break;
            }
            z.swap(nxt);
            window.push_back(z);
            if ((int)window.size() > 27) window.pop_front();
            if ((int)window.size() == 27 && window.front() == window.back()) {
                // period 26 cycle; window[0] == window[26] == current z
                int rem = r - done;
                string s0 = window[0];
                string s1 = window[1];
                int add = rem % 26;
                for (int i = 0; i < m; ++i) {
                    if (s0[i] != s1[i]) {
                        int c = (z[i] - 'a' + add) % 26;
                        z[i] = char('a' + c);
                    }
                }
                finished = true;
                break;
            }
        }
        (void)finished;
        cout << z << '\n';
    }
    return 0;
}
