## 思路

m+n为奇数为Yes，否则为No；

(1) 当m+n为奇数时，m和n必然是一奇一偶，可以选择直接跳到偶数那一边的最后一格子，然后剩奇数格的那条边，这个时候需要跳偶数个单位才能到达死角，而对手只能走奇数个单位，他走之后我们在走奇数个单位即可直接走到死角

(2)当m+n为偶数时，m和n均为奇或偶，无论走几格，都会陷入对方先手的第一种情况，必输

## 代码


### python

```python
t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    if (m + n) % 2 == 1:
        print("Yes")
    else:
        print("No")

```



**c++**

```cpp
#include<bits/stdc++.h>
using namespace std;


int main(){
    int t;cin>>t;
    for(int i=0;i<t;i++){
        int n,m;cin>>n>>m;
        if((n+m)%2==0){
            cout<<"No"<<endl;
        }
        else{
            cout<<"Yes"<<endl;
        }
    }
}
```

**Java**

```java
import java.util.*;

public class Main {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int T = scanner.nextInt();
        for(int t = 0; t < T; t++){
            int n = scanner.nextInt();
            int m = scanner.nextInt();
            if((m + n) % 2 == 1){
                System.out.println("Yes");
            }else System.out.println("No");
        }

    }

}
```