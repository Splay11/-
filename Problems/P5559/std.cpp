#include <iostream>
#include <vector>
using namespace std;

const int V = 1000;

// 二分边长，并用二维前缀和判断某个边长能否框到至少 k 件货
int minSide(int k, const vector<int>& cols, const vector<int>& rows) {
    if (k <= 1) {
        return 1;
    }
    int width = V + 1;
    // 列、行都从 1 编号，把每件货记到对应方格
    vector<int> grid(width * width, 0);
    for (int i = 0; i < (int)cols.size(); i++) {
        grid[cols[i] * width + rows[i]] = 1;
    }
    // ps[c][r] 表示列 1..c、行 1..r 这一块里的件数
    vector<int> ps(width * width, 0);
    for (int c = 1; c <= V; c++) {
        int running = 0;
        int cur = c * width;
        int prev = (c - 1) * width;
        for (int r = 1; r <= V; r++) {
            running += grid[cur + r];
            ps[cur + r] = ps[prev + r] + running;
        }
    }
    auto enough = [&](int side) {
        // 枚举左上角，统计边长为 side 的闭区间里有多少件货
        int span = side - 1;
        int last = V - span;
        for (int c = 1; c <= last; c++) {
            int hi = (c + span) * width;
            int lo = (c - 1) * width;
            for (int r = 1; r <= last; r++) {
                int r2 = r + span;
                int total = ps[hi + r2] - ps[hi + r - 1] - ps[lo + r2] + ps[lo + r - 1];
                if (total >= k) {
                    return true;
                }
            }
        }
        return false;
    };
    // 边长越大越容易凑够 k 件，二分最小可行边长
    int low = 1, high = V;
    while (low < high) {
        int mid = (low + high) / 2;
        if (enough(mid)) {
            high = mid;
        } else {
            low = mid + 1;
        }
    }
    return low;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int k, p;
    cin >> k >> p;
    vector<int> cols(p), rows(p);
    for (int i = 0; i < p; i++) {
        cin >> cols[i];
    }
    for (int i = 0; i < p; i++) {
        cin >> rows[i];
    }
    cout << minSide(k, cols, rows) << '\n';
    return 0;
}
