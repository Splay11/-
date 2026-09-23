#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

// 排序 + 前缀和：每次任务用二分切出小于/大于目标档的两段
vector<long long> minOps(vector<long long> values, const vector<long long>& targets) {
    int m = (int)values.size();
    sort(values.begin(), values.end());
    vector<long long> pref(m + 1, 0);
    for (int i = 0; i < m; i++) {
        pref[i + 1] = pref[i] + values[i];
    }
    // 奇偶个数固定，用来把绝对值之和改成向下取整后的之和
    int odd = 0;
    for (int i = 0; i < m; i++) {
        if (values[i] & 1) {
            odd++;
        }
    }
    int even = m - odd;
    vector<long long> ans;
    ans.reserve(targets.size());
    for (size_t qi = 0; qi < targets.size(); qi++) {
        long long g = targets[qi];
        int lt = (int)(lower_bound(values.begin(), values.end(), g) - values.begin());
        int gt = (int)(upper_bound(values.begin(), values.end(), g) - values.begin());
        long long sumLt = pref[lt];
        long long sumGt = pref[m] - pref[gt];
        int cntGt = m - gt;
        long long sabs = g * lt - sumLt + sumGt - g * cntGt;
        int diff = (g & 1) ? even : odd;
        ans.push_back((sabs - diff) / 2);
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);

    // 先读节点台数和偏移，再读任务条数与每个目标档
    int m;
    cin >> m;
    vector<long long> values(m);
    for (int i = 0; i < m; i++) {
        cin >> values[i];
    }
    int k;
    cin >> k;
    vector<long long> targets(k);
    for (int i = 0; i < k; i++) {
        cin >> targets[i];
    }
    vector<long long> ans = minOps(values, targets);
    // 每项任务单独一行
    for (int i = 0; i < k; i++) {
        cout << ans[i] << "\n";
    }
    return 0;
}
