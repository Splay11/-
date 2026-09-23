#include <iostream>
#include <vector>
#include <sstream>
using namespace std;

// check函数：判断当前值是否符合条件
bool check(int i, const vector<int>& R, int cnt) {
    long long su = 0;
    for (int x : R) {
        su += min(i, x);
    }
    return su <= cnt;
}

int main() {
    // 读入数据
    string line;
    vector<int> R;
    int cnt;

    // 读入数组R
    getline(cin, line);  // 读入整个数组的输入行
    stringstream ss(line);  // 使用stringstream进行分割
    int temp;
    while (ss >> temp) {
        R.push_back(temp);  // 将读取的数字存入R
    }

    // 读入cnt
    cin >> cnt;

    // 二分查找的边界
    int l = 0, r = 1e9;

    // 二分查找
    while (l <= r) {
        int mid = (l + r) >> 1;
        if (check(mid, R, cnt)) {
            l = mid + 1;
        } else {
            r = mid - 1;
        }
    }

    // 这种情况即题目描述的第一种情况，右端点不会动
    if (r == 1e9) {
        r = -1;
    }

    // 输出结果
    cout << r << endl;

    return 0;
}
