# 题解

用哈希表统计对应出现的次数，并对所有出现频次 $\le k$ 的数取最小值即可。

# AC代码

- Python

  ```python
  from collections import defaultdict
  n, k = map(int, input().split())
  d = defaultdict(int)
  a = list(map(int, input().split()))
  for val in a:
      d[val] += 1
  ans = 10 ** 9
  for key, val in d.items():
      if val <= k:
          ans = min(ans, key)
  if ans == 10 ** 9:
      ans = -1
  print(ans)
  
  ```

- C++

  ```cpp
  #include <iostream>
  #include <unordered_map>
  #include <vector>
  #include <climits>
  
  using namespace std;
  
  int main() {
      int n, k;
      cin >> n >> k;
  
      vector<int> a(n);
      unordered_map<int, int> countMap;
  
      for (int i = 0; i < n; ++i) {
          cin >> a[i];
          countMap[a[i]]++;
      }
  
      int ans = INT_MAX;
      for (const auto& entry : countMap) {
          if (entry.second <= k) {
              ans = min(ans, entry.first);
          }
      }
  
      cout << (ans == INT_MAX ? -1 : ans) << endl;
  
      return 0;
  }
  ```

- Java

  ```java
  import java.util.HashMap;
  import java.util.Map;
  import java.util.Scanner;
  
  public class Main {
      public static void main(String[] args) {
          Scanner scanner = new Scanner(System.in);
          int n = scanner.nextInt();
          int k = scanner.nextInt();
          scanner.nextLine();
  
          int[] a = new int[n];
          for (int i = 0; i < n; i++) {
              a[i] = scanner.nextInt();
          }
  
          Map<Integer, Integer> countMap = new HashMap<>();
          for (int val : a) {
              countMap.put(val, countMap.getOrDefault(val, 0) + 1);
          }
  
          int ans = Integer.MAX_VALUE;
          for (Map.Entry<Integer, Integer> entry : countMap.entrySet()) {
              if (entry.getValue() <= k) {
                  ans = Math.min(ans, entry.getKey());
              }
          }
  
          System.out.println(ans == Integer.MAX_VALUE ? -1 : ans);
          scanner.close();
      }
  }
  ```