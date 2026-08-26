## 题解

题意是要求 $n$ 在 $m$ 进制中有多少个 $1$。

按照题意暴力进行模拟就行，总体复杂度为 $O(35 \times \log(n))$

## AC代码

- CPP

  ```cpp
  #include <iostream>
  #include <string>
  #include <algorithm>
  using namespace std;
  
  int main() {
      int n;
      cin >> n;
      
      int ans = 0;
      for (int i = 2; i <= 36; i++) {
          int t = n;
          int cnt = 0;
          while (t) {
              int z = t % i;
              // 统计z转为字符串后包含'1'的个数
              cnt += to_string(z).count('1'); 
              t /= i;
          }
          ans = max(ans, cnt);
      }
      cout << ans << endl;
      return 0;
  }
  ```

- Python

  ```python
  n = int(input())
  ans = 0
  for i in range(2, 37):  # 遍历进制i从2到36
      t, cnt = n, 0
      while t:
          z = t % i       # z是n在i进制下的最低位
          cnt += str(z).count('1')  # 统计z转为字符串后包含'1'的个数
          t //= i         # n整除i,相当于把n在i进制下右移一位
      ans = max(ans, cnt)
  print(ans)
  ```

- Java

  ```java
  import java.util.Scanner;
  
  public class Main {
      public static void main(String[] args) {
          Scanner sc = new Scanner(System.in);
          int n = sc.nextInt();
          
          int ans = 0;
          for (int i = 2; i <= 36; i++) {
              int t = n;
              int cnt = 0;
              while (t > 0) {
                  int z = t % i;
                  // 统计z转为字符串后包含'1'的个数
                  cnt += String.valueOf(z).chars().filter(ch -> ch == '1').count();
                  t /= i;
              }
              ans = Math.max(ans, cnt);
          }
          System.out.println(ans);
      }
  }
  ```