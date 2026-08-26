## 思路

我们通过前缀积来求解。我们$val$表示前缀积，$ne$和$po$分别表示所有前缀积中负数和正数的个数，$ans1$和$ans2$记录答案。假如我们枚举到$i$，此时$val$大于$0$，那么表示$[1,i]$的数组乘积为正，此时由于我们知道$po$和$ne$，由于正数除正数是正数，正数除负数是负数可以知道，有几个$po$就可以有几个$[k,i]$数组乘积为正（$k$是前缀积为正时对应的下标（$K<=i$）），反之$ne$可以知$[k,i]$乘积为负，除此以外，正数的个数还要加1，原因是$[1,i]$也是正数。负数也类似的讨论

## python代码

```python
n = int(input())
arr = list(map(int, input().split()))
val, ne, po, ans1, ans2 = 1, 0, 0, 0, 0
for i in range(n):
    val = val * (1 if arr[i] > 0 else -1)
    if val > 0:
        ans1 += ne
        ans2 += po + 1
    else:
        ans1 += po + 1
        ans2 += ne
    if val > 0:
        po += 1
    else:
        ne += 1
print(ans1, ans2)
# 5
# 5 -3 3 -1 1
```

## C++代码

```C++
#include <bits/stdc++.h>
using namespace std;
const int MAXN = 2e5 + 5;
typedef long long ll;
int n;
int arr[MAXN];
int main(){
	cin >> n;
	for(int i = 1; i <= n; i++)cin >> arr[i];
	int val = 1;
	int ne = 0, po = 0;
	ll ans1 = 0, ans2 = 0;
	for(int i = 1; i <= n; i++){
		val *= arr[i] >= 0? 1 : -1;
		if(val > 0){
			ans1 += ne;
			ans2 += po + 1;
			po++;
		}else{
			ans1 += po + 1;
			ans2 += ne;
			ne++;
		}
	}
	cout << ans1 << " " << ans2 << endl;
}

// 5
// 5 -3 3 -1 1
```