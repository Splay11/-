#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

// 二分消费轮次：每轮全体减 q，被点中的再多减 p-q
bool enough(long long times, const vector<long long>& heat, long long center, long long ambient) {
    long long extra = center - ambient;
    long long need = 0;
    // 先按顺带消费 times 轮，剩下的必须靠主消费补
    long long cooled = ambient * times;
    for (int i = 0; i < (int)heat.size(); i++) {
        long long rest = heat[i] - cooled;
        if (rest > 0) {
            // 向上取整：还要做主消费多少轮
            need += (rest + extra - 1) / extra;
            if (need > times) {
                return false;
            }
        }
    }
    return true;
}

long long min_starts(const vector<long long>& heat, long long center, long long ambient) {
    long long lo = 0, hi = 0;
    for (int i = 0; i < (int)heat.size(); i++) {
        long long w = heat[i];
        // 就算每轮都点它，也至少要 ceil(w/p) 轮
        long long need_center = (w + center - 1) / center;
        if (need_center > lo) {
            lo = need_center;
        }
        // 从不点它、只吃顺带消费，ceil(w/q) 轮一定够
        long long need_amb = (w + ambient - 1) / ambient;
        if (need_amb > hi) {
            hi = need_amb;
        }
    }
    while (lo < hi) {
        long long mid = (lo + hi) / 2;
        if (enough(mid, heat, center, ambient)) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    return lo;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int m;
    cin >> m;
    long long p, q;
    cin >> p >> q;
    vector<long long> w(m);
    for (int i = 0; i < m; i++) {
        cin >> w[i];
    }
    cout << min_starts(w, p, q) << '\n';
    return 0;
}
