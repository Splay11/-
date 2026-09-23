#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

bool can_finish(int c, long long q, long long w, const vector<long long>& h,
                const vector<pair<long long, int>>& freq, long long days) {
    // 判定：在 days 天内能不能打掉 q 块矿岩
    if (days <= 0) {
        return false;
    }
    // days = full 个完整周期 + 多出来的 rest 天
    long long full = days / c;
    int rest = (int)(days % c);
    long long done = 0;
    for (size_t t = 0; t < freq.size(); t++) {
        long long x = freq[t].first;
        long long cnt = freq[t].second;
        long long add;
        if (x <= w) {
            // 初始功率已经够打这个硬度，每个完整周期都能打一次
            add = full;
        } else {
            // 完整周期里功率依次是 w, w+1, ..., w+full-1
            // 要功率 >= x，需要过完 x-w 个周期之后才开始贡献
            add = full - (x - w);
            if (add < 0) {
                add = 0;
            }
        }
        if (add == 0) {
            continue;
        }
        // add * cnt 可能很大，先判断是否已经够 q 块，避免撑爆 long long
        if (add >= q || cnt >= q || add > (q - 1) / cnt) {
            return true;
        }
        done += add * cnt;
        if (done >= q) {
            return true;
        }
    }
    // 多出来的 rest 天功率固定为 w+full，对应周期前 rest 个位置
    long long atk = w + full;
    for (int i = 0; i < rest; i++) {
        if (h[i] <= atk) {
            done++;
            if (done >= q) {
                return true;
            }
        }
    }
    return done >= q;
}

vector<pair<long long, int>> build_freq(vector<long long> h) {
    // 相同硬度合并，二分时只扫不同的硬度值
    sort(h.begin(), h.end());
    vector<pair<long long, int>> freq;
    for (size_t i = 0; i < h.size();) {
        size_t j = i;
        while (j < h.size() && h[j] == h[i]) {
            j++;
        }
        freq.push_back(make_pair(h[i], (int)(j - i)));
        i = j;
    }
    return freq;
}

long long min_days(int c, long long q, long long w, const vector<long long>& h) {
    vector<pair<long long, int>> freq = build_freq(h);
    // 天数越多越容易打完，对天数二分找最小可行值
    long long lo = 1, hi = 4000000000000000000LL, ans = 4000000000000000000LL;
    while (lo <= hi) {
        long long mid = lo + (hi - lo) / 2;
        if (can_finish(c, q, w, h, freq, mid)) {
            ans = mid;
            hi = mid - 1;
        } else {
            lo = mid + 1;
        }
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    int c;
    long long q, w;
    cin >> c >> q >> w;
    vector<long long> h(c);
    for (int i = 0; i < c; i++) {
        cin >> h[i];
    }
    cout << min_days(c, q, w, h) << endl;
    return 0;
}
