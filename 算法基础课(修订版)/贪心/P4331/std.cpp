#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    cin >> T;
    while (T--) {
        int n;
        cin >> n;
        vector<long long> a(n), c(n);
        for (int i = 0; i < n; i++) cin >> a[i];
        for (int i = 0; i < n; i++) cin >> c[i];

        // 点赞数 -> 对应的杂乱度集合
        unordered_map<long long, vector<long long>> mp;
        for (int i = 0; i < n; i++) {
            mp[a[i]].push_back(c[i]);
        }

        // 每个点赞数列表排序（从小到大方便 pop 最大值）
        for (auto &kv : mp) {
            sort(kv.second.begin(), kv.second.end());
        }

        // 所有点赞数按升序排序
        vector<long long> keys;
        keys.reserve(mp.size());
        for (auto &kv : mp) keys.push_back(kv.first);
        sort(keys.begin(), keys.end());

        long long ans = 0;

        // 从后往前贪心成组
        while (!keys.empty()) {
            while (!keys.empty() && mp.find(keys.back()) == mp.end()) {
                keys.pop_back(); // 跳过已空的点赞组
            }
            if (keys.empty()) break;

            long long curMax = 0;
            // 从连续点赞数的末尾往前取
            for (int i = (int)keys.size() - 1; i >= 0; i--) {
                // 如果断开（不连续 或 没有该点赞值的剩余 Plog）
                if (i != (int)keys.size() - 1 && keys[i] != keys[i + 1] - 1) break;
                if (mp.find(keys[i]) == mp.end()) break;

                // 取该点赞组最大杂乱度
                auto &v = mp[keys[i]];
                curMax = max(curMax, v.back());
                v.pop_back();
                if (v.empty()) mp.erase(keys[i]);
            }
            ans += curMax;
        }

        cout << ans << "\n";
    }
    return 0;
}
