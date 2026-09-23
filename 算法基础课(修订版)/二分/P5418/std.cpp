// 有序数组上用二分求 T 的首次/末次出现，以及严格小于/大于 T 的边界下标
#include <iostream>
#include <vector>
using namespace std;

// 返回四个答案：首次、末次、小于 T 的最大下标、大于 T 的最小下标
vector<int> queryPositions(const vector<int>& a, int T) {
    int n = (int)a.size();

    // 求第一个 >= T 的下标（即 lower_bound），找不到则等于 n
    int left = 0, right = n;
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (a[mid] < T) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }
    int lower = left;

    // 求第一个 > T 的下标（即 upper_bound），找不到则等于 n
    left = 0;
    right = n;
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (a[mid] <= T) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }
    int upper = left;

    // T 的首次出现就是 lower；该位置越界或值不是 T 则不存在
    int first = (lower < n && a[lower] == T) ? lower : -1;
    // T 的末次出现就是 upper-1；该位置合法且值是 T 才算找到
    int last = (upper > 0 && a[upper - 1] == T) ? upper - 1 : -1;
    // 小于 T 的数全在 lower 左侧，最大下标是 lower-1
    int pred = (lower > 0) ? lower - 1 : -1;
    // 大于 T 的数从 upper 开始，越界则不存在
    int succ = (upper < n) ? upper : -1;
    return {first, last, pred, succ};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // 第一行：长度与目标值
    int n, T;
    cin >> n >> T;
    // 第二行：非递减数组
    vector<int> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    vector<int> ans = queryPositions(a, T);
    cout << ans[0] << ' ' << ans[1] << ' ' << ans[2] << ' ' << ans[3] << '\n';
    return 0;
}
