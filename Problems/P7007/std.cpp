#include <iostream>
#include <vector>
using namespace std;

bool canReduce(const vector<int>& vals) {
    int lo = vals[0], hi = vals[0];
    for (int x : vals) {
        if (x < lo) lo = x;
        if (x > hi) hi = x;
    }
    vector<char> seen(hi - lo + 1, 0);
    for (int x : vals) seen[x - lo] = 1;
    for (char flag : seen) {
        if (!flag) return false;
    }
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int k;
    cin >> k;
    while (k--) {
        int n;
        cin >> n;
        vector<int> vals(n);
        for (int i = 0; i < n; i++) cin >> vals[i];
        cout << (canReduce(vals) ? "YES" : "NO") << '\n';
    }
    return 0;
}
