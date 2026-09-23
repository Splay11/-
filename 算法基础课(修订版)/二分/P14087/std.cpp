#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);
    
    int n, Q;
    cin >> n >> Q;
    
    vector<long long> arr(n);
    for(auto &x : arr){
        cin >> x;
    }
    
    while(Q--){
        long long target;
        cin >> target;
        
        // 查找比 target 小的最大值
        // upper_bound 返回第一个大于 target 的位置
        // 减一就是最后一个小于或等于 target 的位置
        // 由于需要严格小于 target，所以需要检查 arr[pos -1] < target
        // 如果 arr[pos -1] == target, 需要继续向左查找
        // 但由于数组是升序且元素唯一（假设），可以直接取 pos -1
        // 否则需要调整
        // 为通用性，这里使用 lower_bound 来找到第一个 >= target 的位置
        // 然后 pos -1 就是最后一个 < target 的位置
        int pos_max = lower_bound(arr.begin(), arr.end(), target) - arr.begin() -1;
        long long max_val = (pos_max >=0) ? arr[pos_max] : -1;
        
        // 查找比 target 大的最小值
        // upper_bound 返回第一个大于 target 的位置
        int pos_min = upper_bound(arr.begin(), arr.end(), target) - arr.begin();
        long long min_val = (pos_min < n) ? arr[pos_min] : -1;
        
        cout << max_val << " " << min_val << "\n";
    }
    
    return 0;
}
