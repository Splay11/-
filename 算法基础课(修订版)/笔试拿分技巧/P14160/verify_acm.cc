#include <bits/stdc++.h>
using namespace std;

const int MOD = 1e9 + 7;

struct BIT {
    int size;
    vector<long long> tree;

    BIT(int n) : size(n), tree(n + 1, 0) {}

    void add(int x, long long value) {
        while (x <= size) {
            tree[x] = (tree[x] + value) % MOD;
            x += x & -x;
        }
    }

    long long query(int x) const {
        long long res = 0;
        while (x > 0) {
            res = (res + tree[x]) % MOD;
            x -= x & -x;
        }
        return res;
    }
};

class Solution {
public:
    long long solve(vector<int>& a) {
        vector<int> alls = a;
        sort(alls.begin(), alls.end(), greater<int>());
        alls.erase(unique(alls.begin(), alls.end()), alls.end());

        BIT bit((int)alls.size());
        long long ans = 0;
        for (int x : a) {
            int id = lower_bound(alls.begin(), alls.end(), x, greater<int>()) - alls.begin() + 1;
            long long sum = bit.query(id - 1);
            long long res = (sum + 1) % MOD;
            ans = (ans + res) % MOD;
            bit.add(id, res);
        }
        return ans;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; ++i) {
        cin >> a[i];
    }

    Solution solution;
    cout << solution.solve(a);
    return 0;
}
