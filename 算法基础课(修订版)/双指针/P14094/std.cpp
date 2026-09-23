#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);
    
    int n;
    cin >> n;
    vector<long long> nums(n);
    for(int i=0;i<n;i++) cin >> nums[i];
    long long target;
    cin >> target;
    
    int left = 0;
    int right = n-1;
    while(left < right){
        long long sum = nums[left] + nums[right];
        if(sum == target){
            // 输出下标，从1开始
            cout << left +1 << " " << right +1;
            return 0;
        }
        else if(sum < target){
            left++;
        }
        else{
            right--;
        }
    }
    // 如果没有找到
    cout << -1;
    return 0;
}
