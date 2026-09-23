#include <iostream>
#include <vector>
#include <stack>
using namespace std;

// 计算整数n的十六进制表示中各位数字的和
int compute_weight(int n) {
    if (n == 0) return 0;
    int s = 0;
    while (n > 0) {
        int digit = n & 0xF;  // 获取最低四位
        s += digit;
        n >>= 4;  // 右移四位，处理下一个十六进制数字
    }
    return s;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int N;
    cin >> N;
    
    vector<int> arr(N);
    for (int i = 0; i < N; i++) {
        cin >> arr[i];
    }
    
    // 计算每个元素的权重
    vector<int> weights(N);
    for (int i = 0; i < N; i++) {
        weights[i] = compute_weight(arr[i]);
    }
    
    // 初始化答案数组
    vector<int> answer(N, -1);
    stack<int> stk;
    
    // 从右到左遍历数组
    for (int i = N - 1; i >= 0; i--) {
        // 弹出栈中所有权重小于或等于当前元素权重的元素
        while (!stk.empty() && weights[stk.top()] <= weights[i]) {
            stk.pop();
        }
        // 如果栈不为空，栈顶元素就是右侧第一个权重更大的元素
        if (!stk.empty()) {
            answer[i] = stk.top();
        }
        // 将当前元素的索引压入栈中
        stk.push(i);
    }
    
    // 输出结果
    for (int i = 0; i < N; i++) {
        cout << answer[i];
        if (i < N - 1) cout << " ";
    }
    cout << endl;
    
    return 0;
}
