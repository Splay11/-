#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int maxPathSum(const vector<int>& arr, int index, int n) {
    // 叶子节点的条件：没有左子节点且没有右子节点
    int leftIndex = 2 * index + 1;
    int rightIndex = 2 * index + 2;

    // 如果是叶子节点
    if (leftIndex >= n && rightIndex >= n) {
        return arr[index];
    }

    int leftSum = 0, rightSum = 0;

    // 如果左子树存在，递归计算左子树的最大路径和
    if (leftIndex < n) {
        leftSum = maxPathSum(arr, leftIndex, n);
    }

    // 如果右子树存在，递归计算右子树的最大路径和
    if (rightIndex < n) {
        rightSum = maxPathSum(arr, rightIndex, n);
    }

    // 返回当前节点的值加上左右子树最大路径和
    return arr[index] + max(leftSum, rightSum);
}

int main() {
    int n;
    cin >> n;
    vector<int> arr(n);
    
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }

    // 从根节点开始计算
    cout << maxPathSum(arr, 0, n) << endl;
    
    return 0;
}
