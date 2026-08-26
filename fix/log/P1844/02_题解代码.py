# 题解

看到这种每次能 *2 或 /2 的，操作方案数很多不容易直接做的，就应该往动态规划或者贪心方面去想了。

我们定义 $dp[i][j]$ ，表示对于当前第 $i$ 个数，将其变成 $j$ ，并且保持前 $i$ 数单调不减的最小操作次数。

状态转移：状态可以由 $dp[i - 1]$ 转移过来

- $dp[i][j] = min(dp[i][j], dp[i - 1][k] + cnt)$，其中 $k \le j$ ，$cnt$ 为 $a[i]$ 达到对应的 $j$ 所需的最小操作次数。
- 在转移的时候可以枚举第 $i - 1$ 个数的 $k$ ，对于当前 $a[i]$ 可以用 while 循环维护出到达对应 $j$ 的操作次数。

看起来是一个二维且复杂度能达到 $O(n\times m ^ 2)$ 级别的 DP。

但可以发现每个数只能 乘/除 2，所以 $j$ 的状态数量很有限，大概为 $O(log)$ 级别。

并且其中存在许多 **无效** 状态。

比如对于当前的 $dp[i][j] = X$ 来说，如果存在一个$dp[i][j'] = X'$，其中 $j' \ge j \ and \ X' \ge X$ ，那么$dp[i][j']$ 的存在对于 $dp[i][j]$ 来说是多余的，我们手动去除这种无效状态即可。

最后 dp 数组可以滚动优化成一维

# AC代码

- Python

  ```python
  from collections import defaultdict
  
  n = int(input())
  a = list(map(int, input().split()))
  
  dp = defaultdict(lambda: float('inf'))
  dp[1] = 0
  
  for val in a:
      new_dp = defaultdict(lambda: float('inf'))
      arr = []
  
      for k, v in dp.items():
          l, r = val, val
          cnt = 0
  
          while l >= k: # 除2
              if new_dp[l] == float('inf'):
                  new_dp[l] = v + cnt
                  arr.append(l)
              new_dp[l] = min(new_dp[l], v + cnt)
              l //= 2
              cnt += 1
  
          cnt = 0
          while r < k: # 乘2
              r *= 2
              cnt += 1
          if new_dp[r] == float('inf'):
              new_dp[r] = v + cnt
              arr.append(r)
          new_dp[r] = min(new_dp[r], v + cnt)
  		# 去除无效状态
      arr.sort()
      dp.clear()
      minv = new_dp[arr[0]]
      dp[arr[0]] = minv
  
      for i in range(1, len(arr)):
          if new_dp[arr[i]] > minv:
              continue
          minv = new_dp[arr[i]]
          dp[arr[i]] = minv
  
  res = min(dp.values())
  print(res)
  ```

- C++

  ```cpp
  #include<bits/stdc++.h>
  
  using namespace std;
  
  #define int long long
  signed main (){
      ios::sync_with_stdio(false);
      std::cin.tie(0);
      int n; cin >> n;
      vector<int> a(n);
      for(int& i : a) cin >> i;
      unordered_map<int, int> dp;
      dp[1] = 0; 
      for(int val : a)
      {
          unordered_map<int, int> new_dp;
          vector<int> arr;
          for(auto& [k, v] : dp) 
          {
          	int l = val, r = val;
              int cnt = 0;
              while(l >= k) // 除2
              {
                  if(!new_dp.count(l))
                      new_dp[l] = v + cnt, arr.push_back(l);
                  new_dp[l] = min(new_dp[l], v + cnt);
                  l /= 2;
                  cnt ++ ;
              }
              cnt = 0;
              while(r < k) // 乘2
                  r *= 2, cnt ++;
              if(!new_dp.count(r))
                  new_dp[r] = v + cnt, arr.push_back(r);
              new_dp[r] = min(new_dp[r], v + cnt);
          }
          // 去除无效状态
          sort(arr.begin(), arr.end());
          unordered_map<int, int>().swap(dp);
          int minv = new_dp[arr[0]];
          dp[arr[0]] = minv;
          for(int i = 1; i < arr.size(); i ++)
          {
          	if(new_dp[arr[i]] > minv) continue;
          	minv = new_dp[arr[i]];
          	dp[arr[i]] = minv;
          }
      }
      int res = 1e18;
      for(auto[k, v] : dp)
          res = min(res, v);
      cout << res << "\n";
      return 0;
  }
  ```

- Java

  ```java
  import java.util.*;
  
  public class Main {
      public static void main(String[] args) {
          Scanner scanner = new Scanner(System.in);
          int n = scanner.nextInt();
          long[] a = new long[n];
          for (int i = 0; i < n; i++) {
              a[i] = scanner.nextLong();
          }
  
          Map<Long, Long> dp = new HashMap<>();
          dp.put(1L, 0L);
  
          for (long val : a) {
              Map<Long, Long> newDp = new HashMap<>();
              List<Long> arr = new ArrayList<>();
  
              for (Map.Entry<Long, Long> entry : dp.entrySet()) {
                  long k = entry.getKey();
                  long v = entry.getValue();
  
                  long l = val, r = val;
                  long cnt = 0;
  
                  while (l >= k) { // 除2
                      if (!newDp.containsKey(l)) {
                          newDp.put(l, v + cnt);
                          arr.add(l);
                      }
                      newDp.put(l, Math.min(newDp.get(l), v + cnt));
                      l /= 2;
                      cnt++;
                  }
  
                  cnt = 0;
                  while (r < k) { // 乘2
                      r *= 2;
                      cnt++;
                  }
                  if (!newDp.containsKey(r)) {
                      newDp.put(r, v + cnt);
                      arr.add(r);
                  }
                  newDp.put(r, Math.min(newDp.get(r), v + cnt));
              }
  						// 去除无效状态
              Collections.sort(arr);
              dp.clear();
              long minv = newDp.get(arr.get(0));
              dp.put(arr.get(0), minv);
  
              for (int i = 1; i < arr.size(); i++) {
                  if (newDp.get(arr.get(i)) > minv) continue;
                  minv = newDp.get(arr.get(i));
                  dp.put(arr.get(i), minv);
              }
          }
  
          long res = Long.MAX_VALUE;
          for (long v : dp.values()) {
              res = Math.min(res, v);
          }
  
          System.out.println(res);
          scanner.close();
      }
  }
  ```