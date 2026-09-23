#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
using namespace std;

vector<int> h;  // 服务器高度数组

// 计算区间 [l, r] 的最小代价
int minCost(int l, int r) {
    // 如果左边界大于右边界，返回0（无操作）
    if (l > r) {
        return 0;
    }
    
    // 如果区间只包含一个服务器，返回列操作的代价2
    if (l == r) {
        return 2;  
    }

    // 找到当前区间的最小高度
    int minH = INT_MAX;  
    for (int i = l; i <= r; i++) {
        minH = min(minH, h[i]);  // 更新当前最小高度
    }

    // 进行行操作，初始代价为1秒
    int cost1 = 1;  
    int i = l;  // 从左边界开始遍历
    while (i <= r) {
        // 如果当前服务器的高度大于最小值
        if (h[i] > minH) {
            int start = i;  // 记录当前区间的起始位置
            // 向右移动，直到找到不再大于最小值的服务器
            while (i <= r && h[i] > minH) {
                i++;
            }
            // 对于当前找到的区间，递归计算其代价
            cost1 += minCost(start, i - 1);
        } else {
            // 如果当前服务器高度不大于最小值，继续向右移动
            i++;
        }
    }

    return cost1;  // 返回当前区间的总代价
}

int main() {
    int n;
    cin >> n;  // 输入服务器数量
    h.resize(n + 1);  // 调整数组大小以便使用1-based索引
    for (int i = 1; i <= n; i++) {
        cin >> h[i];  // 输入每个服务器的高度
    }

    cout << minCost(1, n) << endl;  // 输出从1到n的最小检查代价
    return 0;
}
