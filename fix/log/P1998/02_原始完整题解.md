## 思路
&emsp;&emsp;此题n的数据范围最大为7，也就是是说最多有8个数位，在最多选取m个数位的限制下，所有能组合出来的数是有限的，我们可以直接进行枚举，首先在n个数位中枚举选取m个数位的所有情况，用二进制的方式选取，在选取完m个数位后进行dfs，将m个数位所组合出来的所有数字枚举出来，统计有多少个数字大于sum即可
## 代码
### python

```python
def permute(nums):#进行全排列
    ans = []
    n = len(nums)

    def dfs(cur, mask):
        nonlocal ans
        if mask == (1 << n) - 1:
            add = cur[:]
            ans.append(add)
            return

        for i in range(n):
            if (mask >> i) & 1 == 0:
                mask ^= (1 << i)
                cur.append(nums[i])
                dfs(cur, mask)
                cur.pop()
                mask ^= (1 << i)

    dfs([], 0)
    return ans

n, m, k = map(int, input().split())
n += 1
ans = 0

for i in range(1 << n):#枚举选取m个数位
    if bin(i).count('1') == m:#1代表选中
        nums = [j for j in range(n) if i >> j & 1]
        pers = permute(nums)#枚举全排列

        for p in pers:
            if len(p) > 1 and p[0] == 0:
                continue

            num = int(''.join(map(str, p)))
            if num > k:
                ans += 1

print(ans)
```
### java
```java
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Main {
    static List<List<Integer>> permute(int[] nums) {
        List<List<Integer>> ans = new ArrayList<>();
        int n = nums.length;

        dfs(ans, new ArrayList<>(), 0, nums, 0, n);

        return ans;
    }

    static void dfs(List<List<Integer>> ans, List<Integer> cur, int mask, int[] nums, int pos, int n) {
        if (mask == (1 << n) - 1) {
            List<Integer> add = new ArrayList<>(cur);
            ans.add(add);
            return;
        }

        for (int i = 0; i < n; i++) {
            if (((mask >> i) & 1) == 0) {
                mask ^= (1 << i);
                cur.add(nums[i]);
                dfs(ans, cur, mask, nums, i, n);
                cur.remove(cur.size() - 1);
                mask ^= (1 << i);
            }
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        int n = scanner.nextInt();
        int m = scanner.nextInt();
        int k = scanner.nextInt();
        n += 1;
        int ans = 0;

        for (int i = 0; i < (1 << n); i++) {
            if (Integer.bitCount(i) == m) {
                List<Integer> nums = new ArrayList<>();
                for (int j = 0; j < n; j++) {
                    if (((i >> j) & 1) == 1) {
                        nums.add(j);
                    }
                }
                List<List<Integer>> pers = permute(nums.stream().mapToInt(Integer::intValue).toArray());

                for (List<Integer> p : pers) {
                    if (p.size() > 1 && p.get(0) == 0) {
                        continue;
                    }

                    int num = Integer.parseInt(p.stream().map(Object::toString).reduce("", (a, b) -> a + b));
                    if (num > k) {
                        ans++;
                    }
                }
            }
        }

        System.out.println(ans);
    }
}
```
### c++
```cpp
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;
void dfs(vector<vector<int>>& ans, vector<int> cur, int mask, vector<int>& nums, int pos, int n) {
    if (mask == (1 << n) - 1) {
        ans.push_back(cur);
        return;
    }

    for (int i = 0; i < n; i++) {
        if (((mask >> i) & 1) == 0) {
            mask ^= (1 << i);
            cur.push_back(nums[i]);
            dfs(ans, cur, mask, nums, i, n);
            cur.pop_back();
            mask ^= (1 << i);
        }
    }
}
vector<vector<int>> permute(vector<int>& nums) {
    vector<vector<int>> ans;
    int n = nums.size();

    dfs(ans, {}, 0, nums, 0, n);

    return ans;
}

int main() {
    int n, m, k;
    cin >> n >> m >> k;
    n += 1;
    int ans = 0;

    for (int i = 0; i < (1 << n); i++) {
        if (__builtin_popcount(i) == m) {
            vector<int> nums;
            for (int j = 0; j < n; j++) {
                if ((i >> j) & 1) {
                    nums.push_back(j);
                }
            }
            vector<vector<int>> pers = permute(nums);

            for (const auto& p : pers) {
                if (p.size() > 1 && p[0] == 0) {
                    continue;
                }

                int num = 0;
                for (int digit : p) {
                    num = num * 10 + digit;
                }

                if (num > k) {
                    ans++;
                }
            }
        }
    }

    cout << ans << endl;

    return 0;
}
```