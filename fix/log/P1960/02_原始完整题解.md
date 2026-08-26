## 题目思路

从后往前做异或和，每次让第i个元素和后面的所有元素相等，后面处理过的元素是不会再改变了，前面累计异或的值可以用一个值来维护。

如果当前元素和累计异或值异或之后还是不等于最后一个元素，就将答案加一。

## 代码


**C++**

~~~cpp
#include <iostream>  
#include <vector>  
using namespace std;  
  
int solve(vector<int>& a) {  
    int cnt = 0;  
    int s = 0;  
    for (int i = a.size() - 2; i >= 0; --i) {  
        if ((a[i] ^ s) != a[a.size() - 1]) {  
            cnt++;  
            s ^= a[i] ^ s ^ a[a.size() - 1];  
        }  
    }  
    return cnt;  
}  
  
int main() {  
    int t;  
    cin >> t;  
    while (t-- > 0) {  
        int n;  
        cin >> n;  
        vector<int> arr(n);  
        for (int i = 0; i < n; ++i) {  
            cin >> arr[i];  
        }  
        cout << solve(arr) << endl;  
    }  
    return 0;  
}
~~~

### **Python**
``` Python

n = int(input())
for _ in range(n):
    size = int(input())
    nums = list(map(int, input().split()))
    t = 0
    for j in range(size - 1):
        if nums[j] == nums[j + 1]:
            if j == size - 2:
                t += 1
            t += 1
    if t == 0:
        print(size - 1)
    else:
        print(size - t)
**会员可通过查看《已通过》的提交记录来查看其他语言哦~**