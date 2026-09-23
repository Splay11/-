#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

// 枚举第二种操作次数；全体先按满击中算点名，再把豁免分到代价最小的位置
long long cost_with_type2(const vector<long long>& load, long long heavy, long long light, long long type2) {
    int n = (int)load.size();
    long long t0_sum = 0;
    vector<long long> t0(n), slack(n);
    for (int i = 0; i < n; i++) {
        long long x = load[i];
        // 先假设每个数都被第二种操作打中 type2 次
        long long rest = x - light * type2;
        if (rest > 0) {
            long long need = (rest + heavy - 1) / heavy;
            t0_sum += need;
            t0[i] = need;
            slack[i] = 0;
        } else {
            t0[i] = 0;
            if (x <= 0) {
                slack[i] = type2;
            } else {
                long long need_b = (x + light - 1) / light;
                slack[i] = max(0LL, type2 - need_b);
            }
        }
    }
    // 第二种操作必须选中某几个下标共 type2 次，这些下标当次不会被减 B
    long long free_slot = 0;
    for (int i = 0; i < n; i++) {
        free_slot += slack[i];
    }
    if (free_slot >= type2) {
        return type2 + t0_sum;
    }
    long long extra = type2 - free_slot;
    long long best_delta = -1;
    for (int i = 0; i < n; i++) {
        long long used = slack[i] + extra;
        if (used > type2) {
            continue;
        }
        long long hits = type2 - used;
        long long rest = load[i] - light * hits;
        long long need = rest <= 0 ? 0 : (rest + heavy - 1) / heavy;
        long long delta = need - t0[i];
        if (best_delta < 0 || delta < best_delta) {
            best_delta = delta;
        }
    }
    if (best_delta < 0) {
        return (1LL << 60);
    }
    return type2 + t0_sum + best_delta;
}

long long min_ops(const vector<long long>& load, long long heavy, long long light) {
    int n = (int)load.size();
    long long only_a = 0;
    for (int i = 0; i < n; i++) {
        if (load[i] > 0) {
            only_a += (load[i] + heavy - 1) / heavy;
        }
    }
    if (n == 1) {
        return only_a;
    }
    long long max_need = 0, sum_need = 0;
    for (int i = 0; i < n; i++) {
        long long need_b = 0;
        if (load[i] > 0) {
            need_b = (load[i] + light - 1) / light;
        }
        if (need_b > max_need) {
            max_need = need_b;
        }
        sum_need += need_b;
    }
    long long max_s = max(max_need, (sum_need + n - 2) / (n - 1));
    long long best = only_a;
    // S 再大也比只减 A 更亏
    if (max_s > only_a) {
        max_s = only_a;
    }
    for (long long type2 = 0; type2 <= max_s; type2++) {
        long long cur = cost_with_type2(load, heavy, light, type2);
        if (cur < best) {
            best = cur;
        }
    }
    return best;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    long long heavy, light;
    cin >> heavy >> light;
    vector<long long> load(n);
    for (int i = 0; i < n; i++) {
        cin >> load[i];
    }
    cout << min_ops(load, heavy, light) << '\n';
    return 0;
}
