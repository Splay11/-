#include <bits/stdc++.h>
using namespace std;

// 统计二进制数组中至多有 k 个 1 的子数组数量
long long countAtMostK(const vector<int>& b, int k) {
    int left = 0;
    long long result = 0;
    int count = 0;
    for(int right = 0; right < b.size(); ++right){
        if(b[right] == 1){
            count++;
        }
        while(count > k){
            if(b[left] == 1){
                count--;
            }
            left++;
        }
        result += (right - left + 1);
    }
    return result;
}

int main(){
    // 读取第一行，整数序列 a
    string line;
    getline(cin, line);
    vector<int> a;
    int num;
    stringstream ss(line);
    while(ss >> num){
        a.push_back(num);
    }
    
    // 读取第二行，x 和 k
    int x, k;
    cin >> x >> k;
    
    // 将 a 映射为二进制数组 b，1 表示能被 x 整除，0 否则
    vector<int> b(a.size(), 0);
    for(int i = 0; i < a.size(); ++i){
        if(a[i] % x == 0){
            b[i] = 1;
        }
    }
    
    // 计算答案
    long long total = countAtMostK(b, k);
    if(k > 0){
        total -= countAtMostK(b, k-1);
    }
    cout << total;
    return 0;
}
