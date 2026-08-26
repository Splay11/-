## 题目思路

考虑一种特殊情况，当从a选出来的值都一样时，可以将a提取出来使得两边相等，同理，b也是一样。

通过打表发现，只有当从a或者b中取出的元素都相同时才有可能左右相等，所以直接求a和b中最大的出现次数即可。

## 代码


**C++**

~~~cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  int T;
  cin >> T;
  while (T--) {
    int n;
    cin >> n;
    vector<int> a(n), b(n);
    map<int, int> ma, mb;
    for (int i = 0; i < n; ++i) {
      cin >> a[i];
      ++ma[a[i]];
    }
    for (int i = 0; i < n; ++i) {
      cin >> b[i];
      ++mb[b[i]];
    }
    int ans = 0;
    for (int i = 0; i < n; ++i) {
      ans = max({ans, ma[a[i]], mb[b[i]]});
    }
    cout << ans << endl;
  }
}

~~~


### java
~~~java
import java.util.*;
public class Main{
    public static void main(String[] args) {
        Scanner in =new Scanner(System.in);
        int T=in.nextInt();
        while(T-->0){
            int n=in.nextInt();
            int ans =1;
            Map<Integer,Integer> cntA=new HashMap<>();
            for(int i=0;i<n;i++){
                int a =in.nextInt();
                cntA.put(a,cntA.getOrDefault(a, 0)+1);
                ans=Math.max(ans,cntA.get(a));
            }
            Map<Integer,Integer> cntB=new HashMap<>();
            for(int i=0;i<n;i++){
                int b =in.nextInt();
                cntB.put(b,cntB.getOrDefault(b, 0)+1);
                ans=Math.max(ans,cntB.get(b));
            }
            System.out.println(ans);
        }
    }
}
**会员可通过查看《已通过》的提交记录来查看其他语言哦~**