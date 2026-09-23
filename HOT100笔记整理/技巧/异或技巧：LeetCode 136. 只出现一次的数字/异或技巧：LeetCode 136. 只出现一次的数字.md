## LeetCode 136. 只出现一次的数字

[在线刷题](https://codefun2000.com/p/P4035)

给你一个非空 整数数组 $nums$ ，除了某个元素只出现一次以外，其余每个元素均出现两次。找出那个只出现了一次的元素。

你必须设计并实现线性时间复杂度的算法来解决此问题，且该算法只使用常量额外空间。

**输入** 

```
4 1 2 1 2
```

**输出** 

```
4
```

**思路**

**异或的特性:相同的数异或 = 0** 

例如:$1 \oplus 1 = 0 , 5\oplus 5 =0 , 1\oplus5 \oplus 1 \oplus 5 = 0$

有了这个性质，我们可以将所有数都异或起来，相同的数会被抵消，最后剩下的即为只出现一次的数。
#code-switcher
```python
from typing import List

class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        ans = 0
        # 遍历每个数字，利用异或运算抵消成对出现的数
        for num in nums:
            ans ^= num  # ans = ans XOR num
        return ans
```
```cpp
class Solution {
public:
    // 功能函数：找出数组中只出现一次的数字
    int singleNumber(vector<int>& nums) {
        int ans = 0;
        // 遍历每个数字，利用异或运算抵消成对出现的数
        for (int num : nums) {
            ans ^= num; // ans = ans XOR num
        }
        return ans;
    }
};
```
```java
class Solution {
    public int singleNumber(int[] nums) {
        int ans = 0;
        // 遍历每个数字，利用异或运算抵消成对出现的数
        for (int num : nums) {
            ans ^= num; // ans = ans XOR num
        }
        return ans;
    }
}
```

```go
func singleNumber(nums []int) int {
	ans := 0
	for _, num := range nums {
		ans ^= num
	}
	return ans
}
```

```javascript
/**
 * @param {number[]} nums
 * @return {number}
 */
var singleNumber = function (nums) {
    let ans = 0;
    for (const num of nums) {
        ans ^= num;
    }
    return ans;
};

```

```c
int singleNumber(int* nums, int numsSize) {
    int ans = 0;
    for (int i = 0; i < numsSize; ++i) {
        ans ^= nums[i];
    }
    return ans;
}

```

#code-switcher
### 面试问答

**1. 本题的核心思路是什么？**

利用异或的<相同的数异或为0>的特性，将所有数都异或起来，相同的数会被抵消，最后剩下的即为只出现一次的数