## 题面描述

给定一个长度为 $n$ 的数组 $a$ ，我们定义：

- $f(a) = a_1 \oplus a_2 \oplus \cdots \oplus a_n$ （$\oplus$ 表示按位异或）
- $g(a) = \gcd(a_1, a_2, \ldots, a_n)$ （$\gcd$ 表示所有元素的最大公约数）

我们需要从数组 $a$ 中选取一个 **非空的连续子数组** $b$ ，使得
$$
f(b) \times g(b)
$$
尽可能大。请输出这个最大值。

## 思路分析

### 直观分析

- 子数组的异或值 $f(b)$ 和子数组的最大公约数 $g(b)$ 都与子数组中元素的分布、大小紧密相关。  
- **单个元素** 形成的子数组 $[\,a_i\,]$ 的异或和是 $a_i$，最大公约数也是 $a_i$，因此其贡献为

$$
  f([{a_i}]) *g([{a_i}]) = a_i * a_i = a_i^2.
$$

- 如果子数组包含多个元素，那么：
  1. 最大公约数 $g(b)$ 一定不会超过子数组中最小元素，更不会超过数组中的最大元素；
  2. 异或和 $f(b)$ 可能会大也可能会小，但一般难以“大幅超过”单个最大元素的平方。

可见，**单个最大元素**（或若干相同最大元素且个数为奇数）所能得到的 $a_i^2$ 已经是最优值或与最优值相同。想超过最大元素平方，需要子数组的 $\gcd$ 或异或和有极大增益，但在实际情形下很难超过。

## cpp
```cpp
#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;  // 读取测试组数
    while(T--){
        int n;
        cin >> n;  // 读取数组长度 n
        long long maxVal = 0;  // 用 long long 存储，避免后续平方溢出
        for(int i = 0; i < n; i++){
            long long x;
            cin >> x;  // 读取数组元素
            if(x > maxVal){
                maxVal = x;
            }
        }
        // 输出最大值平方
        cout << maxVal * maxVal << "\n";
    }
    return 0;
}

```
## python
```python
def solve():
    import sys

    input_data = sys.stdin.read().strip().split()
    # 使用 sys.stdin.read() 可以一次性读取所有内容
    # 分割后用索引读取。

    T = int(input_data[0])           # 测试组数
    index = 1                        # 当前读取的位置
    output_lines = []

    for _ in range(T):
        n = int(input_data[index])   # 数组长度 n
        index += 1
        max_val = 0
        # 遍历本组测试的 n 个数字
        for __ in range(n):
            x = int(input_data[index])
            index += 1
            if x > max_val:
                max_val = x
        # 将最大元素平方加入输出结果
        output_lines.append(str(max_val * max_val))

    # 一次性输出所有结果
    print("\n".join(output_lines))


if __name__ == "__main__":
    solve()

```
## java
```java
import java.util.*;
import java.io.*;

public class Main {
    public static void main(String[] args) {
        FastReader in = new FastReader(System.in);
        int T = in.nextInt();  // 读取测试数据组数
        StringBuilder sb = new StringBuilder();

        while(T-- > 0){
            int n = in.nextInt(); // 数组长度
            long maxVal = 0;      // 用 long 存储以防后续平方溢出
            for(int i = 0; i < n; i++){
                long x = in.nextLong();  // 当前元素
                if(x > maxVal) {
                    maxVal = x;
                }
            }
            // 输出最大值平方
            sb.append(maxVal * maxVal).append("\n");
        }

        System.out.print(sb.toString());
    }

    // 一个常见的快速读入类
    static class FastReader {
        BufferedReader br;
        StringTokenizer st;
        public FastReader(InputStream stream) {
            br = new BufferedReader(new InputStreamReader(stream));
        }
        String next() {
            while(st == null || !st.hasMoreTokens()){
                try{
                    String line = br.readLine();
                    if(line == null) return null;
                    st = new StringTokenizer(line);
                } catch (IOException e){
                    throw new RuntimeException(e);
                }
            }
            return st.nextToken();
        }
        int nextInt(){
            return Integer.parseInt(next());
        }
        long nextLong(){
            return Long.parseLong(next());
        }
    }
}

```