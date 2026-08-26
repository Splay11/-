## 题目思路

首先如果所有行的异或和不等于所有列的异或和那说明无解。

考虑构造，将2到n行的第一列元素都放置对应的行异或值，将2到m列的第一行元素都放置对应的列异或值，其余置为0。

而第一行第一列的值等于可以通过第一列的列异或值和2-n行的行异或值异或得到，也可以通过第一行的行异或值和2-m列的列异或值异或得到，这两种肯定都一样，因为行异或和等于列异或和。

## 代码


**C++**

~~~cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  int n, m;
  cin >> n >> m;
  vector<vector<int>> ans(n, vector<int> (m, 0));
  int row = 0, col = 0;
  for (int i = 0, x;i < n;++ i) {
  	cin >> x;
  	ans[i][0] = x;
  	row ^= x;
  }
  for (int i = 0, x;i < m;++ i) {
  	cin >> x;
  	if (i) {
  		ans[0][i] = x;
  	} 
  	col ^= x;
  }
  if (row != col) {
  	puts("NO");
  } else {
  	puts("YES");
  	for (int i = 1;i < m;++ i) ans[0][0] ^= ans[0][i];
  	for (int i = 0;i < n;++ i) {
  		for (int j = 0;j < m;++ j) {
  			cout << ans[i][j] << " \n"[j == m - 1];
  		}
  	}
  }
}

~~~

**会员可通过查看《已通过》的提交记录来查看其他语言哦~**