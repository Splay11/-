#include <iostream>
#include <algorithm>
using namespace std;

// 两个轴对齐矩形面积之和减去重叠
int solve(int ax1, int ay1, int ax2, int ay2,
          int bx1, int by1, int bx2, int by2) {
    long long area_a = 1LL * (ax2 - ax1) * (ay2 - ay1);
    long long area_b = 1LL * (bx2 - bx1) * (by2 - by1);
    int w = min(ax2, bx2) - max(ax1, bx1);
    int h = min(ay2, by2) - max(ay1, by1);
    long long overlap = 0;
    if (w > 0 && h > 0) {
        overlap = 1LL * w * h;
    }
    return (int)(area_a + area_b - overlap);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int ax1, ay1, ax2, ay2, bx1, by1, bx2, by2;
    cin >> ax1 >> ay1 >> ax2 >> ay2 >> bx1 >> by1 >> bx2 >> by2;
    cout << solve(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2) << '\n';
    return 0;
}
