#warning-box

**必做前置题** ： [数组上的快慢指针-LeetCode 283.移动零](https://codefun2000.com/codenote/hot100/P0015#leetcode-283.移动零)

#warning-box

[在线刷题](https://codefun2000.com/p/P4101)

给定一个长度为 $n$ 的数组 `nums`，其中包含 **红色**、**白色** 和 **蓝色** 三种颜色，分别用整数 `0`、`1` 和 `2` 表示。请对 `nums` 进行 **原地排序**，使得相同颜色的元素相邻，并按 **红色、白色、蓝色** 顺序排列。

要求 **不使用** 内置排序函数。

**输入** 

```
6
2 0 2 1 1 0
```

**输出** 

```
0 0 1 1 2 2
```

**思路**

## **做法一：两趟遍历 + 快慢指针**

做了前置题，一个很显然的做法是正反扫两遍，第一遍正着扫，把0放到数组前缀。 第二遍反着扫，把2放到数组后缀。

**这里我们用一个动画来为大家演示👇**
@[video](https://codefun2000.com/p/4202/file/%E4%B8%A4%E9%81%8D%E9%81%8D%E5%8E%86.mp4)

#code-switcher
```python
from typing import List
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        n = len(nums)
        # 正着循环 ， 将0 放到前面
        i , j = 0 , 0
        for i in range(n):
            if nums[i] == 0:
                nums[i] , nums[j] = nums[j] , nums[i]
                j += 1
        # 倒着循环 ， 将2 放到后面
        i , j = n - 1 , n - 1
        for i in range(n - 1, -1, -1):
            if nums[i] == 2:
                nums[i] , nums[j] = nums[j] , nums[i]
                j -= 1
        return nums
```
```cpp
class Solution {
public:
    vector<int> sortColors(vector<int>& nums) {
        int n = nums.size();

        // 正着循环 ， 将0 放到前面
        int i, j;
        i = 0, j = 0;
        for (i = 0; i < n; i++) {
            if (nums[i] == 0) {
                swap(nums[i], nums[j]);
                j += 1;
            }
        }

        // 倒着循环 ， 将2 放到后面
        i = n - 1, j = n - 1;
        for (i = n - 1; i >= 0; i--) {
            if (nums[i] == 2) {
                swap(nums[i], nums[j]);
                j -= 1;
            }
        }

        return nums;
    }
};
```
```java
class Solution {
    public int[] sortColors(int[] nums) {
        int n = nums.length;

        // 正着循环 ， 将0 放到前面
        int i, j;
        i = 0;
        j = 0;
        for (i = 0; i < n; i++) {
            if (nums[i] == 0) {
                int temp = nums[i];
                nums[i] = nums[j];
                nums[j] = temp;
                j += 1;
            }
        }

        // 倒着循环 ， 将2 放到后面
        i = n - 1;
        j = n - 1;
        for (i = n - 1; i >= 0; i--) {
            if (nums[i] == 2) {
                int temp = nums[i];
                nums[i] = nums[j];
                nums[j] = temp;
                j -= 1;
            }
        }

        return nums;
    }
}
```


```javascript
/**
 * @param {number[]} nums
 * @return {void}
 */
var sortColors = function (nums) {
    const n = nums.length;
    // 正着循环，将 0 放到前面
    let j = 0;
    for (let i = 0; i < n; i++) {
        if (nums[i] === 0) {
            [nums[i], nums[j]] = [nums[j], nums[i]];
            j++;
        }
    }
    // 倒着循环，将 2 放到后面
    j = n - 1;
    for (let i = n - 1; i >= 0; i--) {
        if (nums[i] === 2) {
            [nums[i], nums[j]] = [nums[j], nums[i]];
            j--;
        }
    }
};

```

```c
void sortColors(int* nums, int numsSize) {
    // 正着循环，将 0 放到前面
    int j = 0;
    for (int i = 0; i < numsSize; ++i) {
        if (nums[i] == 0) {
            int tmp = nums[i];
            nums[i] = nums[j];
            nums[j] = tmp;
            ++j;
        }
    }
    // 倒着循环，将 2 放到后面
    j = numsSize - 1;
    for (int i = numsSize - 1; i >= 0; --i) {
        if (nums[i] == 2) {
            int tmp = nums[i];
            nums[i] = nums[j];
            nums[j] = tmp;
            --j;
        }
    }
}
```

```go
func sortColors(nums []int) {
	n := len(nums)
	// 正着循环，将 0 放到前面
	j := 0
	for i := 0; i < n; i++ {
		if nums[i] == 0 {
			nums[i], nums[j] = nums[j], nums[i]
			j++
		}
	}
	// 倒着循环，将 2 放到后面
	j = n - 1
	for i := n - 1; i >= 0; i-- {
		if nums[i] == 2 {
			nums[i], nums[j] = nums[j], nums[i]
			j--
		}
	}
}

```

#code-switcher
## **做法二：一趟遍历 + 快慢指针**

可以将两趟遍历优化成一趟遍历。从左往右扫，遇到0放到前缀，遇到2放到后缀。

有一个特殊情况需要注意：`2 1 0` , 在第一步变成了:`0 1 2` ， **此时将`2`放到后缀的时候，恰好也把一个`0`放到正确的位置上了。此时不仅后缀指针往前移动，前缀指针也需要往后移动一位**。 


**这里我们用一个动画来为大家演示👇**
@[video](https://codefun2000.com/p/4202/file/%E4%B8%80%E9%81%8D%E9%81%8D%E5%8E%86.mp4)


#code-switcher
```python
from typing import List

class Solution:
    def sortColors(self, nums: List[int]) -> None:
        # 两遍遍历法 , j 用来记录前缀0的边界 , k 用来记录后缀2的边界
        j, k = 0, len(nums) - 1
        n = len(nums)
        i = 0

        # 遍历数组
        while i <= k:
            # 如果当前元素为0 , 则将其放到前面
            if nums[i] == 0:
                nums[i], nums[j] = nums[j], nums[i]
                j += 1
                i += 1

            # 如果当前元素为2 , 则将其放到后面
            elif nums[i] == 2:
                nums[i], nums[k] = nums[k], nums[i]
                k -= 1
                # 这里不需要 i += 1 , 因为例如 2 1 0 这种情况 , 交换完之后 变成 0 1 2 , 需要继续判断当前元素是否为0，如果是0，则需要j += 1

            # 如果当前元素为1 , 则不需要处理
            else:
                i += 1

        return nums
      
```
```cpp
class Solution {
public:
    vector<int> sortColors(vector<int>& nums) {
        // 两遍遍历法 , j 用来记录前缀0的边界 , k 用来记录后缀2的边界
        int j = 0, k = nums.size() - 1;
        int n = nums.size();
        int i = 0;

        // 遍历数组
        while (i <= k) {
            // 如果当前元素为0 , 则将其放到前面
            if (nums[i] == 0) {
                swap(nums[i], nums[j]);
                j += 1;
                i += 1;
            }
            // 如果当前元素为2 , 则将其放到后面
            else if (nums[i] == 2) {
                swap(nums[i], nums[k]);
                k -= 1;
                // 这里不需要 i += 1 , 因为例如 2 1 0 这种情况 , 交换完之后 变成 0 1 2 , 需要继续判断当前元素是否为0，如果是0，则需要j += 1
            }
            // 如果当前元素为1 , 则不需要处理
            else {
                i += 1;
            }
        }

        return nums;
    }
};

```
```java
class Solution {
    public int[] sortColors(int[] nums) {
        // 两遍遍历法 , j 用来记录前缀0的边界 , k 用来记录后缀2的边界
        int j = 0, k = nums.length - 1;
        int n = nums.length;
        int i = 0;

        // 遍历数组
        while (i <= k) {
            // 如果当前元素为0 , 则将其放到前面
            if (nums[i] == 0) {
                int temp = nums[i];
                nums[i] = nums[j];
                nums[j] = temp;
                j += 1;
                i += 1;
            }
            // 如果当前元素为2 , 则将其放到后面
            else if (nums[i] == 2) {
                int temp = nums[i];
                nums[i] = nums[k];
                nums[k] = temp;
                k -= 1;
                // 这里不需要 i += 1 , 因为例如 2 1 0 这种情况 , 交换完之后 变成 0 1 2 , 需要继续判断当前元素是否为0，如果是0，则需要j += 1
            }
            // 如果当前元素为1 , 则不需要处理
            else {
                i += 1;
            }
        }

        return nums;
    }
}
```

```c
void sortColors(int* nums, int numsSize) {
    // 一遍遍历法：j 记录前缀 0 的边界，k 记录后缀 2 的边界
    int j = 0, k = numsSize - 1;
    int i = 0;
    // 遍历数组
    while (i <= k) {
        // 当前元素为 0，换到前面
        if (nums[i] == 0) {
            int tmp = nums[i];
            nums[i] = nums[j];
            nums[j] = tmp;
            ++j;
            ++i;
        }
        // 当前元素为 2，换到后面
        else if (nums[i] == 2) {
            int tmp = nums[i];
            nums[i] = nums[k];
            nums[k] = tmp;
            --k;
            /* 此处不 ++i：例如 2 1 0 交换后变成 0 1 2，需继续判断换入的 0 */
        }
        // 当前元素为 1，无需处理
        else {
            ++i;
        }
    }
}
```

```go
func sortColors(nums []int) {
	// 一遍遍历法：j 记录前缀 0 的边界，k 记录后缀 2 的边界
	j, k := 0, len(nums)-1
	i := 0
	// 遍历数组
	for i <= k {
		// 当前元素为 0，换到前面
		if nums[i] == 0 {
			nums[i], nums[j] = nums[j], nums[i]
			j++
			i++
		} else if nums[i] == 2 {
			// 当前元素为 2，换到后面
			nums[i], nums[k] = nums[k], nums[i]
			k--
			// 此处不 i++：例如 2 1 0 交换后变成 0 1 2，需继续判断换入的 0
		} else {
			// 当前元素为 1，无需处理
			i++
		}
	}
}
```

```javascript
/**
 * @param {number[]} nums
 * @return {void}
 */
var sortColors = function (nums) {
    // 一遍遍历法：j 记录前缀 0 的边界，k 记录后缀 2 的边界
    let j = 0, k = nums.length - 1;
    let i = 0;
    // 遍历数组
    while (i <= k) {
        // 当前元素为 0，换到前面
        if (nums[i] === 0) {
            [nums[i], nums[j]] = [nums[j], nums[i]];
            j++;
            i++;
        }
        // 当前元素为 2，换到后面
        else if (nums[i] === 2) {
            [nums[i], nums[k]] = [nums[k], nums[i]];
            k--;
            // 此处不 i++：例如 2 1 0 交换后变成 0 1 2，需继续判断换入的 0
        }
        // 当前元素为 1，无需处理
        else {
            i++;
        }
    }
};
```

#code-switcher
## 面试问答

**1. 本题的核心思路是什么？**

**快慢指针思想**。我们可以维护三个区域：前面全是 0，并用`left`来维护已经处理好的`0`区，后面全是 2，并用`right`来维护已经处理好的`2`区，中间是还没处理的数。指针 `i` 负责扫描 , 看到 0 就丢到前面，看到 2 就丢到后面，看到 1 就跳过。唯一需要注意的是，2 和右边交换之后，换回来的数字还不知道是什么，所以 `i` 不能马上右移，要继续检查当前位置,如果是0则还需要让`left`右移。这样一趟遍历就能把三种颜色排好。