#include <iostream>
#include <vector>
using namespace std;

int pivotIndex(const vector<int>& nums) {
    // 求整个数组的总和（本题范围 int 够用，这里用 long long 更稳妥）
    long long total = 0;
    for (int x : nums) {
        total += x;
    }
    // leftSum 表示当前下标左侧所有元素之和；下标 0 的左侧没有元素，初值为 0
    long long leftSum = 0;
    for (int i = 0; i < (int)nums.size(); i++) {
        // 右侧元素之和 = 总和 - 左侧和 - 当前元素
        // （当前元素是中心下标所指的元素，既不算左侧也不算右侧）
        long long rightSum = total - leftSum - nums[i];
        if (leftSum == rightSum) {
            // 从前往后扫描，第一个满足条件的位置就是最靠左的中心下标
            return i;
        }
        // 当前位置不是中心下标，把当前元素并入左侧，继续考察下一个位置
        leftSum += nums[i];
    }
    // 扫完整个数组仍未找到，说明不存在中心下标
    return -1;
}

int main() {
    // 关闭流同步，加快大量整数的读入
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // 第一行：数组长度 n
    int n;
    cin >> n;
    // 第二行：n 个整数
    vector<int> nums(n);
    for (int i = 0; i < n; i++) {
        cin >> nums[i];
    }

    // 输出最靠左的中心下标，不存在则为 -1
    cout << pivotIndex(nums) << "\n";
    return 0;
}
