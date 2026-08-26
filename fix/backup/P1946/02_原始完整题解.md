## 思路：状态压缩动态规划

前置知识:[二进制集合操作](https://oi-wiki.org/math/binary-set/) , 动态规划

考虑如果一个数Ai存在超集，那么Ai可以被删掉。考虑求解dp[x]含义为x的超集是否存在，使用状态压缩动态规划套路进行转移。查询dp[Ai]来删除数.

转移方程为:$dp[i] |= dp[j] or (j \in A)$ , 其中j是二进制位恰好比i多一个的所有数.A是数组集合.

其他细节全部写在代码注释里了，大家查看!

## 代码
### python
```python
# 定义位的长度
bit_len = 18 
# 定义二进制数的最大值
all_bits = 1 << bit_len 
n = int(input())
arr = list(map(int, input().split()))
# 记录是否有某个二进制数
has_bits = [False] * all_bits 
for x in arr:
    has_bits[x] = True
# dp[x]记录是否存在x的超集
dp = [False] * all_bits
# 从大到小遍历所有的二进制数
for i in range(all_bits - 1, -1 , -1):
    # 以此往x里添加一个1
    for j in range(bit_len):
        # 如果x的第j位是0 , 尝试往i里插入1到这个位置并转移
        if i & (1 << j) == 0:
            # 如果x的<恰好多一个bit>的数存在超集或者x的<恰好多一个bit>的数本身存在
            dp[i] = dp[i] or (dp[i | (1 << j)] or has_bits[i | (1 << j)])

'''
正确性阐述:这里大家可能疑问的一点是:为什么可以就<恰好多一个bit>的转移。如果是<恰好多k个的情况>呢?(k > 1)
首先,按照从大到小的顺序遍历的,所以在遍历到x的时候,所有的x的超集（因为x的超集在数值上 > x）都已经被转移过了。
所以x的<恰好多了k个bit>的超集在x的<恰好多了k-1个bit>的时候就是传给他true了，那么k-1->k-2->...->1都是传递的true。
例如:
存在Ai = 1101
那么1001就是true
那么在转移1000的时候,因为1001是true,所以1000也是true。所以对于1000的情况(以及所有其他x)，我们只需要考虑<恰好多一个bit>的情况就可以了。
'''
# 计算答案 , 记得先给数去重
st = list(set(arr))
ans = len(st)
for x in st:
    # 如果x的超集存在
    if dp[x]:
        ans -= 1
print(ans)
```
### Java
```Java
import java.util.*;
class Main {
    public static void main(String[] args) {
            int bitLen = 18;
            int allBits = 1 << 18;
            Scanner sc = new Scanner(System.in);
            int n = sc.nextInt();
            int[] arr = new int[n];
            for (int i = 0; i < n; i++) {
                arr[i] = sc.nextInt();
            }
            boolean[] hasBits = new boolean[allBits];
            for (int i = 0; i < n; i++) {
                hasBits[arr[i]] = true;
            }
            boolean[] dp = new boolean[allBits];
            for (int i = allBits - 1; i >= 0; i--) {
                for (int j = 0; j < bitLen; j++) {
                    if ((i & (1 << j)) == 0) {
                        dp[i] = dp[i] || dp[i | (1 << j)] || hasBits[i | (1 << j)];
                    }

                }
            }
            Set<Integer> unique = new HashSet<>();
            for (int x : arr) {
                unique.add(x);
            }
            int ans = unique.size();
            for (int x : unique) {
                if (dp[x]) {
                    ans--;
                }
            }
            System.out.println(ans);






    }


}
```
### C++
``` C++
#include <iostream>
#include <cstring>
#include <cstdio>
#include <algorithm>

using namespace std;

const int N = 200010, M = 300010;

int a[N];
bool st[M], f[M];
int n;

int main()
{
    scanf("%d", &n);
    for (int i = 1; i <= n; i ++)
    {
        scanf("%d", &a[i]);
        st[a[i]] = 1;
    }
    
    for (int i = (1 << 18) - 1; i >= 0; i --)
        for (int j = 0; j < 18; j ++)
            if ((i & (1 << j)) == 0)
            {
                f[i] = f[i] | f[i | (1 << j)] | st[i | (1 << j)];
            }
    
    sort(a + 1, a + n + 1);
    int m = unique(a + 1, a + n + 1) - a - 1;
    
    int ans = m;
    for (int i = 1; i <= m; i ++)
        if (f[a[i]])
            ans --;
    printf("%d\n", ans);
    
    return 0;
}
```
OJ会员可以通过点击题目上方《已通过》查看其他通过代码来学习。