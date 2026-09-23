#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    while (q--) {
        int m;
        long long t;
        cin >> m >> t;
        vector<int> out;
        int s = m;
        while (s >= 1) {
            if (t >= s - 1 && s > 1) {
                out.push_back(s); // 放最大值，贡献 s-1
                t -= s - 1;
                --s;
            } else {
                if (t == 0) {
                    for (int i = 1; i <= s; ++i) out.push_back(i);
                } else {
                    out.push_back((int)t + 1);
                    for (int i = 1; i <= t; ++i) out.push_back(i);
                    for (int i = (int)t + 2; i <= s; ++i) out.push_back(i);
                }
                break;
            }
        }
        for (int i = 0; i < (int)out.size(); ++i) {
            if (i) cout << ' ';
            cout << out[i];
        }
        cout << '\n';
    }
    return 0;
}
