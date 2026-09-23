#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    string s;
    cin >> n >> s;

    long long tot = 0, wrap = 0;
    long long freq[26] = {0};

    for (int i = 1; i <= n; i++) {
        tot += i;
        int k = s[i-1] - 'a';
        wrap += freq[k] + 1;   // 增量 f+1
        freq[k]++;
        cout << tot - wrap << "\n";
    }
    return 0;
}
