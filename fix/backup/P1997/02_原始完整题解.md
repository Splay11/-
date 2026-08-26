## 思路
&emsp;&emsp;此题是一个三维动态规划问题，只要想到了状态如何表示，那么状态之间的转移其实是比较简单的，首先这里对于字符串的操作其实就是选定字符串的一个前缀将前缀里的1与0全部翻转，在只有这种操作下，我们要将一个字符串变为全1最小的操作次数其实就是从右往左，只要碰到0就将其翻转，选定的前缀逐渐变小，这是一个贪心的操作，也是最优，这是解题的基础

&emsp;&emsp;设置dp[i][j][k]，定义为以下表i结尾，长度为奇或偶，权值为奇或偶的子字符串的个数，0表示偶，1表示奇，状态转移分三种情况
1. 当前位为1，无需操作，直接从前一位的奇偶状态转移
2. 当前位为0但与前一位一致，同样无需额外操作，直接从前一位的奇偶状态转移
3. 当前位为0但与前一位不一致，此处需要两次操作（使此处变1后前一位在操作一次使前面的位数回到原来状态），奇偶状态不变转移

（从状态转移规律可以进行思考，其实可以得出一个结论，以1开头的字符串权值一定为偶，以0开头的字符串权值一定为奇，至于结论如何得来，可以仔细思考思考）
## 代码
### python

```python
n = int(input())
s = input()

dp = [[[0, 0] for _ in range(2)] for _ in range(n)]
ans = 0

for i in range(n):
    if s[i] == '1':
        dp[i][1][0] += 1
        if i > 0:
            dp[i][0][0] += dp[i - 1][1][0]
            dp[i][0][1] += dp[i - 1][1][1]
            dp[i][1][0] += dp[i - 1][0][0]
            dp[i][1][1] += dp[i - 1][0][1]
    else:
        dp[i][1][1] += 1
        if i > 0:
            if s[i - 1] == s[i]:
                dp[i][0][0] += dp[i - 1][1][0]
                dp[i][0][1] += dp[i - 1][1][1]
                dp[i][1][0] += dp[i - 1][0][0]
                dp[i][1][1] += dp[i - 1][0][1]
            else:
                dp[i][0][0] += dp[i - 1][1][0]
                dp[i][0][1] += dp[i - 1][1][1]
                dp[i][1][0] += dp[i - 1][0][0]
                dp[i][1][1] += dp[i - 1][0][1]

    ans += dp[i][1][1]

print(ans)
```
### java
```java
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        int n = scanner.nextInt();
        String s = scanner.next();

        int[][][] dp = new int[n][2][2];
        int ans = 0;

        for (int i = 0; i < n; i++) {
            if (s.charAt(i) == '1') {
                dp[i][1][0] += 1;
                if (i > 0) {
                    dp[i][0][0] += dp[i - 1][1][0];
                    dp[i][0][1] += dp[i - 1][1][1];
                    dp[i][1][0] += dp[i - 1][0][0];
                    dp[i][1][1] += dp[i - 1][0][1];
                }
            } else {
                dp[i][1][1] += 1;
                if (i > 0) {
                    if (s.charAt(i - 1) == s.charAt(i)) {
                        dp[i][0][0] += dp[i - 1][1][0];
                        dp[i][0][1] += dp[i - 1][1][1];
                        dp[i][1][0] += dp[i - 1][0][0];
                        dp[i][1][1] += dp[i - 1][0][1];
                    } else {
                        dp[i][0][0] += dp[i - 1][1][0];
                        dp[i][0][1] += dp[i - 1][1][1];
                        dp[i][1][0] += dp[i - 1][0][0];
                        dp[i][1][1] += dp[i - 1][0][1];
                    }
                }
            }

            ans += dp[i][1][1];
        }

        System.out.println(ans);
    }
}
```
### c++
```cpp
#include <iostream>
#include <vector>

using namespace std;

int main() {
    int n;
    cin >> n;
    string s;
    cin >> s;

    vector<vector<vector<int>>> dp(n, vector<vector<int>>(2, vector<int>(2, 0)));
    int ans = 0;

    for (int i = 0; i < n; i++) {
        if (s[i] == '1') {
            dp[i][1][0] += 1;
            if (i > 0) {
                dp[i][0][0] += dp[i - 1][1][0];
                dp[i][0][1] += dp[i - 1][1][1];
                dp[i][1][0] += dp[i - 1][0][0];
                dp[i][1][1] += dp[i - 1][0][1];
            }
        } else {
            dp[i][1][1] += 1;
            if (i > 0) {
                if (s[i - 1] == s[i]) {
                    dp[i][0][0] += dp[i - 1][1][0];
                    dp[i][0][1] += dp[i - 1][1][1];
                    dp[i][1][0] += dp[i - 1][0][0];
                    dp[i][1][1] += dp[i - 1][0][1];
                } else {
                    dp[i][0][0] += dp[i - 1][1][0];
                    dp[i][0][1] += dp[i - 1][1][1];
                    dp[i][1][0] += dp[i - 1][0][0];
                    dp[i][1][1] += dp[i - 1][0][1];
                }
            }
        }

        ans += dp[i][1][1];
    }

    cout << ans << endl;

    return 0;
}
```