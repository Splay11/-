#include <vector>
#include <cmath>
#include <unordered_map>
#include <unordered_set>
using namespace std;

class Solution {
public:
    int minShareOps(vector<int>& pieces) {
        int n = (int)pieces.size();
        if (n < 2) return 0;
        int mx = pieces[0];
        for (int v : pieces) if (v > mx) mx = v;
        mx += 1;
        vector<int> spf(mx + 1);
        for (int i = 0; i <= mx; i++) spf[i] = i;
        for (int i = 2; i * i <= mx; i++) {
            if (spf[i] == i) {
                for (int j = i * i; j <= mx; j += i) {
                    if (spf[j] == j) spf[j] = i;
                }
            }
        }
        auto factors = [&](int x) {
            unordered_set<int> s;
            while (x > 1) {
                int p = spf[x];
                s.insert(p);
                while (x % p == 0) x /= p;
            }
            return s;
        };
        unordered_map<int, int> cnt;
        vector<unordered_set<int>> facs(n);
        for (int i = 0; i < n; i++) {
            facs[i] = factors(pieces[i]);
            for (int p : facs[i]) cnt[p]++;
        }
        for (auto& kv : cnt) {
            if (kv.second >= 2) return 0;
        }
        for (int i = 0; i < n; i++) {
            auto fs = factors(pieces[i] + 1);
            for (int p : fs) {
                if (facs[i].count(p)) {
                    if (cnt[p] >= 2) return 1;
                } else if (cnt[p] >= 1) {
                    return 1;
                }
            }
        }
        return 2;
    }
};
