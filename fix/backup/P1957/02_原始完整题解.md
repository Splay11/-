## 题目思路

直接枚举摆放多少行的地砖，由于最好是上下和左右都联通，所以优先摆放为矩形是最优的，多出来的可以摆放到最后一列又或者最后一行。

然后求这个摆放有多少的圆即可，最后取最大值。

## 代码


**Python**

~~~python
n = int(input())
ans = n - 1

for i in range(1, n + 1):
    j = n // i
    k = n % i
    if k > 0:
        k = 2 * k - 1
    ans = max(ans, (i - 1) * j + (j - 1) * i + k)

print(ans)
~~~


### Python
``` Python
import java.io.*;
import java.util.*;
public class Main {
    public static String line;
    public static String[] parts;
    public static long res = 0;
    public static void main(String[] args) throws IOException {
        BufferedReader bf = new BufferedReader(new InputStreamReader(System.in));
        StreamTokenizer in = new StreamTokenizer(bf);
        PrintWriter out = new PrintWriter(new OutputStreamWriter(System.out));
        int n = Integer.valueOf(bf.readLine());
        int res = n - 1;
        for(int i = 2; i <= n; i++){
            int j = n / i;
            int rest = n % i;
            if(rest > 0){
                res = Math.max(res, (i - 1) * j + (j - 1) * i + 2 * rest - 1);
            }else{
                res = Math.max(res, (i - 1) * j + (j - 1) * i);
            }

        }
        out.println(res);
        out.flush();
    }
}
```
### C++
``` C++
#include <iostream>
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n = 0;
    cin >> n;
    int ans = n - 1;
    for (int i = 2; i < n; ++ i) {
        int j = n / i;
        int k = n % i;
        ans = max(ans, k + k - 1 + (i - 1) * j + (j - 1) * i);
    }
    cout << ans << endl;
    return 0;
}
```
**会员可通过查看《已通过》的提交记录来查看其他语言哦~**