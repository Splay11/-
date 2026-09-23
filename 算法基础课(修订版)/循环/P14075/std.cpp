#include <iostream>  
#include <vector>    
using namespace std;

int main() {
    int n;  // 定义整数 n，用于存储数组的大小
    cin >> n;  // 从标准输入读取数组大小

    vector<int> arr(n);  // 创建一个大小为 n 的向量 arr，用来存储输入的数组元素
    for (int i = 0; i < n; i++) {
        cin >> arr[i];  // 从标准输入读取数组的元素
    }

    int max_value = arr[0];  // 初始化最大值为数组的第一个元素
    vector<int> indices;  // 创建一个空的向量 indices，用于存储最大值出现的下标

    // 第一个循环：找出数组中的最大值
    for (int i = 0; i < n; i++) {
       max_value = max(max_value, arr[i]);  // max是自带的库，比较两者的最大值
    }

    // 第二个循环：找出所有等于最大值的下标
    for (int i = 0; i < n; i++) {
        bool mk = (arr[i] == max_value ? 1 : 0);  // 如果当前元素等于最大值，则 mk 为 1
        if (mk) indices.push_back(i);  // 如果 mk 为 1，说明当前元素等于最大值，将其下标加入 indices 向量
    }

    // 输出最大值
    cout << max_value << endl;

    // 输出所有最大值的下标
    for (int i = 0; i < indices.size(); i++) {
        cout << indices[i] << (i == indices.size() - 1 ? "" : " ");  // 输出下标，并且确保最后一个下标后不加空格
    }
    cout << endl;  // 输出换行符

    return 0;  // 程序执行完毕，返回 0
}
