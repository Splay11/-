#include<bits/stdc++.h>
using namespace std;

// 定义一个结构体来存储商品的重量、价值和单位重量的价值
struct Item {
    int weight;
    int value;
    double ratio;
};

// 比较函数，用于按照单位重量价值降序排序
bool compare(const Item &a, const Item &b) {
    return a.ratio > b.ratio;
}

// 分数背包问题的解决方案
double fractional_knapsack(int n, int C, vector<pair<int, int>> &items) {
    // 存储商品的重量、价值和单位重量的价值
    vector<Item> items_with_ratio;
    
    for (int i = 0; i < n; ++i) {
        int weight = items[i].first;
        int value = items[i].second;
        double ratio = (double)value / weight;  // 计算单位重量的价值
        items_with_ratio.push_back({weight, value, ratio});
    }
    
    // 按照单位重量价值从大到小排序
    sort(items_with_ratio.begin(), items_with_ratio.end(), compare);
    
    double total_value = 0.0;  // 总价值初始化为0
    int remaining_capacity = C;  // 剩余背包容量
    
    for (const auto &item : items_with_ratio) {
        if (remaining_capacity == 0) {  // 背包已满
            break;
        }
        if (item.weight <= remaining_capacity) {  // 商品能完全放入背包
            total_value += item.value;
            remaining_capacity -= item.weight;
        } else {  // 只能放入部分商品
            total_value += item.value * ((double)remaining_capacity / item.weight);
            remaining_capacity = 0;  // 背包满了
        }
    }
    
    return total_value;
}

int main() {
    int n, C;
    cin >> n >> C;  // 读取商品数量n和背包最大承重C
    
    vector<pair<int, int>> items;
    for (int i = 0; i < n; ++i) {
        int w, v;
        cin >> w >> v;  // 读取每个商品的重量w和价值v
        items.push_back({w, v});
    }
    
    // 计算并输出结果，保留两位小数
    double result = fractional_knapsack(n, C, items);
    cout << fixed << setprecision(2) << result << endl;
    
    return 0;
}
