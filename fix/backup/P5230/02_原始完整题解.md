## 解题思路

最终要求整个数组的最大公约数大于 $1$。

假设最终所有元素都有一个公共因数 $d>1$，那么 $d$ 一定至少包含一个质因数 $p$。因此，最终所有元素也一定都能被某个质数 $p$ 整除。

对于一个固定的质数 $p$：

* 原数组中已经能被 $p$ 整除的元素可以直接保留。
* 不能被 $p$ 整除的元素需要修改成 $p$ 的倍数。
* 如果有 $cnt_p$ 个元素能被 $p$ 整除，那么需要修改的次数就是

$$
n-cnt_p
$$

所以问题转化为：

> 找到一个质数 $p$，使原数组中能被 $p$ 整除的元素数量最多。

设这个最大数量为 $mx$，答案就是

$$
n-mx
$$

具体实现时，先统计每个数出现的次数。然后使用埃氏筛求出不超过数组最大值的所有质数。

对于每个质数 $p$，枚举它的所有倍数

$$
p,2p,3p,\ldots
$$

累加这些数在数组中的出现次数，就可以得到能被 $p$ 整除的元素数量。

特别地，元素 $1$ 不会被任何质数整除，因此不会被统计进去。

## 复杂度分析

设数组中的最大值为 $M$。

使用埃氏筛求质数的时间复杂度为

$$
O(M\log\log M)
$$

对于所有质数枚举其倍数，总时间复杂度同样为

$$
O(M\log\log M)
$$

统计数组元素需要 $O(n)$ 的时间。

因此总时间复杂度为

$$
O(n+M\log\log M)
$$

空间复杂度为

$$
O(M)
$$

在 $n\le 120000$、$M\le 900000$ 的数据范围下可以通过。

## 代码实现

### Python

```python
def min_operations(n, nums):
    max_value = max(nums)

    # 统计每个数出现的次数
    freq = [0] * (max_value + 1)
    for x in nums:
        freq[x] += 1

    # 埃氏筛求质数
    is_prime = [True] * (max_value + 1)
    if max_value >= 0:
        is_prime[0] = False
    if max_value >= 1:
        is_prime[1] = False

    i = 2
    while i * i <= max_value:
        if is_prime[i]:
            j = i * i
            while j <= max_value:
                is_prime[j] = False
                j += i
        i += 1

    # 统计每个质数能整除多少个数组元素
    max_count = 0

    for p in range(2, max_value + 1):
        if is_prime[p]:
            count = 0

            # 枚举质数 p 的所有倍数
            for multiple in range(p, max_value + 1, p):
                count += freq[multiple]

            max_count = max(max_count, count)

    return n - max_count


def main():
    n = int(input())
    nums = list(map(int, input().split()))

    print(min_operations(n, nums))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {

    public static int minOperations(int[] nums) {
        int n = nums.length;
        int maxValue = 0;

        for (int x : nums) {
            maxValue = Math.max(maxValue, x);
        }

        // 统计每个数出现的次数
        int[] freq = new int[maxValue + 1];
        for (int x : nums) {
            freq[x]++;
        }

        // 埃氏筛求质数
        boolean[] isPrime = new boolean[maxValue + 1];
        Arrays.fill(isPrime, true);

        if (maxValue >= 0) {
            isPrime[0] = false;
        }
        if (maxValue >= 1) {
            isPrime[1] = false;
        }

        for (int i = 2; i * i <= maxValue; i++) {
            if (isPrime[i]) {
                for (int j = i * i; j <= maxValue; j += i) {
                    isPrime[j] = false;
                }
            }
        }

        int maxCount = 0;

        // 枚举每个质数
        for (int p = 2; p <= maxValue; p++) {
            if (isPrime[p]) {
                int count = 0;

                // 枚举质数 p 的所有倍数
                for (int multiple = p; multiple <= maxValue; multiple += p) {
                    count += freq[multiple];
                }

                maxCount = Math.max(maxCount, count);
            }
        }

        return n - maxCount;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        int n = Integer.parseInt(br.readLine().trim());
        int[] nums = new int[n];

        int index = 0;
        StringTokenizer st = null;

        while (index < n) {
            if (st == null || !st.hasMoreTokens()) {
                st = new StringTokenizer(br.readLine());
            }
            nums[index++] = Integer.parseInt(st.nextToken());
        }

        System.out.println(minOperations(nums));
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int minOperations(const vector<int>& nums) {
    int n = nums.size();
    int maxValue = *max_element(nums.begin(), nums.end());

    // 统计每个数出现的次数
    vector<int> freq(maxValue + 1, 0);
    for (int x : nums) {
        freq[x]++;
    }

    // 埃氏筛求质数
    vector<bool> isPrime(maxValue + 1, true);

    if (maxValue >= 0) {
        isPrime[0] = false;
    }
    if (maxValue >= 1) {
        isPrime[1] = false;
    }

    for (int i = 2; i * i <= maxValue; i++) {
        if (isPrime[i]) {
            for (int j = i * i; j <= maxValue; j += i) {
                isPrime[j] = false;
            }
        }
    }

    int maxCount = 0;

    // 枚举每个质数
    for (int p = 2; p <= maxValue; p++) {
        if (isPrime[p]) {
            int count = 0;

            // 枚举质数 p 的所有倍数
            for (int multiple = p; multiple <= maxValue; multiple += p) {
                count += freq[multiple];
            }

            maxCount = max(maxCount, count);
        }
    }

    return n - maxCount;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<int> nums(n);
    for (int i = 0; i < n; i++) {
        cin >> nums[i];
    }

    cout << minOperations(nums) << '\n';

    return 0;
}
```