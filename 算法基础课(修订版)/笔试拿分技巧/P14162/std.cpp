#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>

using namespace std;

int main() {
    int n, k; // 输入博览会的数量n和每次可以参加的博览会数量k
    cin >> n >> k;
    
    vector<vector<int>> a(n, vector<int>(2)); // 用于存储博览会的开始和结束时间
    for (int i = 0; i < n; i++) {
        cin >> a[i][0] >> a[i][1]; // 读取开始和结束时间
    }

    // 根据开始时间排序
    sort(a.begin(), a.end(), [](const vector<int>& x, const vector<int>& y) {
        return x[0] < y[0];
    });

    int start = 0; // 当前时间
    priority_queue<int, vector<int>, greater<int>> queue; // 最小堆用于存储结束时间
    int idx = 0; // 当前处理的博览会索引
    int ans = 0; // 参加的博览会数量

    while (idx < n || !queue.empty()) {
        // 移除已结束的博览会
        while (!queue.empty() && queue.top() < start) {
            queue.pop();
        }

        // 添加当前可以参加的博览会
        while (idx < n && a[idx][0] <= start) {
            queue.push(a[idx][1]); // 将结束时间加入优先队列
            idx++;
        }

        // 如果没有可参加的博览会，更新开始时间
        if (queue.empty()) {
            if (idx == n) {
                break;
            }
            start = max(start, a[idx][0]);
        }
        while (idx < n && a[idx][0] <= start){
            queue.push(a[idx][1]);
            idx++;
        }
        // 参加博览会
        for (int i = 0; i < k; i++) {
            if (!queue.empty()) {
                ans++; // 参加博览会
                queue.pop(); // 弹出结束时间
            }
        }

        start++; // 增加当前时间
    }

    cout << ans << endl; // 输出参加的博览会数量
    return 0; // 结束程序
}
