#include <iostream>
using namespace std;

// check函数：判断是否能合成mid套砖块
bool check(int a, int b, int c, int mid, int x, int y) {
    int a1 = a, b1 = b, c1 = c;

    // 尝试从红砖合成蓝砖
    if (a1 > mid) {
        int f = (a1 - mid) / x;  // 计算多余的红砖能合成多少蓝砖
        a1 -= x * f;  // 消耗掉这些红砖
        b1 += f;  // 增加蓝砖的数量
    }

    // 尝试从蓝砖合成绿砖
    if (b1 > mid) {
        int f = (b1 - mid) / y;  // 计算多余的蓝砖能合成多少绿砖
        b1 -= y * f;  // 消耗掉这些蓝砖
        c1 += f;  // 增加绿砖的数量
    }

    return a1 >= mid && b1 >= mid && c1 >= mid;
}

int main() {
    // 读取测试数据的组数
    int T;
    cin >> T;

    // 遍历每一组数据
    while (T--) {
        // 读取每组数据
        int a, b, c, x, y;
        cin >> a >> b >> c >> x >> y;

        // 二分查找的左边界和右边界
        int l = 0, r = 1e9;

        // 二分查找
        while (l < r) {
            int mid = (l + r + 1) / 2;  // 尝试获取的中间套数

            // 如果经过合成后，红砖、蓝砖、绿砖都能满足mid套，则可以尝试更大的mid
            if (check(a, b, c, mid, x, y)) {
                l = mid;
            } else {
                r = mid - 1;  // 否则尝试更小的mid
            }
        }

        // 输出结果，即最多可以收集到的砖块套数
        cout << l << endl;
    }

    return 0;
}
