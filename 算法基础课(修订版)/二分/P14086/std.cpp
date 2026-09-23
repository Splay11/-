#include <iostream>
#include <vector>
#include <algorithm>  // 包含lower_bound和upper_bound
using namespace std;

int main() {
    int n, Q;
    cin >> n >> Q;
    vector<int> A(n);
    
    for (int i = 0; i < n; ++i) {
        cin >> A[i];
    }
    
    while (Q--) {
        int x;
        cin >> x;
        
        // 使用 lower_bound 查找第一个大于等于 x 的位置
        auto first = lower_bound(A.begin(), A.end(), x);
        // 使用 upper_bound 查找第一个大于 x 的位置
        auto last = upper_bound(A.begin(), A.end(), x);
        
        // 判断元素是否存在
        if (first != A.end() && *first == x) {
            // 如果存在，输出第一次和最后一次出现的位置
            cout << (first - A.begin() + 1) << " " << (last - A.begin()) << endl;
        } else {
            // 如果不存在，输出 -1 -1
            cout << -1 << " " << -1 << endl;
        }
    }

    return 0;
}
