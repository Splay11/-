# 题解

记 `zero` 和 `one`为 最后一个 0/1 的下标 ，初始值为 -1。

遍历字符串，每次记录 1 和 0 的最新下标，并将其不同字符的最后一个下标加入答案。

# AC代码

- Python

  ```python
  T = int(input()) 
  for _ in range(T):
      n = int(input())
      s = input()
      zero, one = -1, -1
      ans = []
      for i in range(n):
          if s[i] == '1':
              ans.append(zero)
              one = i + 1
          else:
              ans.append(one)
              zero = i + 1
      print(' '.join(map(str, ans)))
  ```

- C++

  ```cpp
  #include <iostream>
  #include <vector>
  #include <string>
  
  using namespace std;
  
  int main() {
      int T;
      cin >> T;
  
      while (T--) {
          int n;
          cin >> n;
          string s;
          cin >> s;
  
          int zero = -1, one = -1;
          vector<int> ans(n);
  
          for (int i = 0; i < n; ++i) {
              if (s[i] == '1') {
                  ans[i] = zero;
                  one = i + 1;
              } else {
                  ans[i] = one;
                  zero = i + 1;
              }
          }
  
          for (int i = 0; i < n; ++i) {
              cout << ans[i];
              if (i < n - 1) {
                  cout << " ";
              }
          }
          cout << endl;
      }
  
      return 0;
  }
  ```

- Java

  ```java
  import java.util.Scanner;
  
  public class Main {
      public static void main(String[] args) {
          Scanner scanner = new Scanner(System.in);
          int T = scanner.nextInt();
          scanner.nextLine();
  
          for (int t = 0; t < T; t++) {
              int n = scanner.nextInt();
              scanner.nextLine();
              String s = scanner.nextLine();
  
              int zero = -1, one = -1;
              int[] ans = new int[n];
  
              for (int i = 0; i < n; i++) {
                  if (s.charAt(i) == '1') {
                      ans[i] = zero;
                      one = i + 1;
                  } else {
                      ans[i] = one;
                      zero = i + 1;
                  }
              }
  
              for (int i = 0; i < n; i++) {
                  System.out.print(ans[i]);
                  if (i < n - 1) {
                      System.out.print(" ");
                  }
              }
              System.out.println();
          }
  
          scanner.close();
      }
  }
  ```