## 思路：模拟

我们可以定义一个长度为2的字符串数组$s$，然后根据题意，分奇偶两种情况模拟即可，具体参考下面代码



**C++**

```cpp
#include<bits/stdc++.h>
using namespace std;
int n;
int main(){
    vector<string>s={"you","uoy"};
    cin>>n;
    for(int i=0;i<n;i++){
        if(i%2==0)cout<<s[0];
        else cout<<s[1];
    }
    return 0;
}
```