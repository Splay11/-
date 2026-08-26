# 题解 
 
## 题目概述
题目要求统计一个字符串中所有满足条件的非空子串数量。条件是：子串去重后，其字符按照相对顺序排列在字典序上是一个单调递增的字符串。
 
例如，字符串 `aabca` 去重后为 `abc`，满足字典序单调递增，因此 `aabca` 是一个好字符串。我们需要计算所有这样的子串数量。
 
## 解题思路 
1. **去重与字典序**：子串去重后，字符按照它们在原字符串中的顺序排列，且必须满足字典序递增。这意味着去重后的子串中的字符必须是严格递增的。
2. **子串的贡献**：对于每个字符 `s[left]`，我们需要找到以它为左端点的所有满足条件的子串。这些子串的右端点必须满足以下条件：
   - 从 `left` 到右端点之间的字符去重后，字符是严格递增的。
   - 右端点必须小于等于某个特定的位置，以确保子串的去重后字符是递增的。
3. **逆序遍历**：为了高效计算每个字符的贡献，我们可以逆序遍历字符串，维护每个字符最后一次出现的位置。通过这种方式，我们可以快速找到满足条件的右端点范围。
4. **从 'z' 到 'a' 遍历**：
从字典序最大的字符开始遍历，确保右端点的选择满足字符严格递增的条件。
5. **计算贡献**：对于每个字符 `s[left]`，我们计算以它为左端点的所有满足条件的子串数量，并累加到答案中。
## 具体步骤
1. **逆序遍历字符串：**
从字符串末尾开始遍历，更新每个字符的最后出现位置。
2. **遍历字符集：**
从 'z' 到 'a' 遍历字符集，动态更新右边界 right 和限制值 limit。
right = min(right, lastPos[j])：确保右端点不超过当前字符的最后出现位置。
limit = min(limit, lastPos[j])：确保右端点的选择不会破坏字符严格递增的条件。
3. **累加贡献：**
以 left 为左端点的子串数量为 limit - left，累加到答案中。
## 代码实现 

**python**
```python
def count_good_substrings(n, s):
    last_pos = {chr(ord('a') + i): -1 for i in range(26)}  # 记录每个字符最后一次出现的位置 ，-1表示未出现
    ans = 0  # 记录满足条件的子串数量 
 
    # 逆序遍历字符串，计算贡献 
    for left in range(n - 1, -1, -1):
        last_pos[s[left]] = left  # 更新当前字符的最后出现位置 
        right = n  # 初始化右边界 
        limit = n  # 初始化限制值 
 
        # 遍历所有字符，找到满足条件的右端点 
        for c in sorted(last_pos.keys(),  reverse=True):
            if last_pos[c] != -1:  # 如果字符出现过 
                if right < last_pos[c]:
                    limit = min(limit, last_pos[c])
                right = min(right, last_pos[c])
        ans += limit - left  # 累加以 left 为左端点的子串数量 
 
    return ans 
 
n = int(input())
s = input()
print(count_good_substrings(n, s))  
```
**c++**
 
```cpp 
#include <bits/stdc++.h>
using namespace std;
 
int main() {
    int n;
    string s;
    cin >> n >> s;
    long long ans = 0;
    vector<int> last_pos(26, -1); // 记录每个字符最后一次出现的位置，初始化为 -1
 
    // 逆序遍历字符串，计算贡献 
    for (int left = n - 1; left >= 0; left--) {
        last_pos[s[left] - 'a'] = left; // 更新当前字符的最后出现位置 
        int right = n, limit = n; // 初始化右边界和限制值 
 
        // 遍历所有字符，找到满足条件的右端点 
        for (int j = 25; j >= 0; j--) {
            if (last_pos[j] != -1) { // 如果字符出现过 
                if (right < last_pos[j]) limit = min(limit, last_pos[j]);
                right = min(right, last_pos[j]); 
            }
        }
        ans += limit - left; // 累加以 left 为左端点的子串数量 
    }
    cout << ans << '\n';
    return 0;
}
```
**java**
```java
import java.util.*; 
 
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in); 
        int n = sc.nextInt(); 
        String s = sc.next(); 
        long ans = 0;
        int[] lastPos = new int[26]; // 记录每个字符最后一次出现的位置 
        Arrays.fill(lastPos,  -1); // 初始化为 -1
 
        // 逆序遍历字符串，计算贡献 
        for (int left = n - 1; left >= 0; left--) {
            lastPos[s.charAt(left) - 'a'] = left; // 更新当前字符的最后出现位置 
            int right = n, limit = n; // 初始化右边界和限制值 
 
            // 遍历所有字符，找到满足条件的右端点 
            for (int j = 25; j >= 0; j--) {
                if (lastPos[j] != -1) { // 如果字符出现过 
                    if (right < lastPos[j]) limit = Math.min(limit,  lastPos[j]);
                    right = Math.min(right,  lastPos[j]);
                }
            }
            ans += limit - left; // 累加以 left 为左端点的子串数量 
        }
        System.out.println(ans); 
    }
}
```