#include <iostream>
#include <vector>
using namespace std;

// 计算最大利润的函数
int maxProfit(const vector<int>& prices) {
    int max_profit = 0;

    // 遍历价格数组，从第二天开始与前一天进行比较
    for (int i = 1; i < prices.size(); ++i) {
        // 如果今天的价格比昨天高，则可以获得利润
        if (prices[i] > prices[i - 1]) {
            // 累加利润
            max_profit += prices[i] - prices[i - 1];
        }
    }

    return max_profit;
}

int main() {
    int n;
    cin >> n;  // 获取数组长度
    vector<int> prices(n);
    
    for (int i = 0; i < n; ++i) {
        cin >> prices[i];  // 获取价格数组
    }

    // 输出最大利润
    cout << maxProfit(prices) << endl;

    return 0;
}
