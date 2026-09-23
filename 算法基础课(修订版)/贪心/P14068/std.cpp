#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

// 计算最少硬币数的函数
int minCoins(vector<int>& coins, int amount) {
    // 将硬币按面额从大到小排序
    sort(coins.rbegin(), coins.rend());

    // 初始化硬币数目
    int coin_count = 0;

    // 遍历硬币，尝试从大到小使用硬币
    for (int coin : coins) {
        if (amount == 0) {
            break;
        }
        // 使用尽可能多的当前硬币
        coin_count += amount / coin;
        amount %= coin;  // 更新剩余金额
    }

    // 如果amount变为0，说明找到了最小硬币数
    if (amount == 0) {
        return coin_count;
    } else {
        return -1;  // 如果无法组合成目标金额，返回-1
    }
}

int main() {
    int n;
    cin >> n;  // 输入硬币数量
    vector<int> coins(n);
    
    for (int i = 0; i < n; ++i) {
        cin >> coins[i];  // 输入硬币面额
    }
    
    int amount;
    cin >> amount;  // 输入目标金额

    // 输出最少硬币数
    cout << minCoins(coins, amount) << endl;

    return 0;
}
