## 题解

## 题目描述

工厂被划分为 $m$ 个片区，工厂内安装了 $n$ 个摄像头。每个摄像头监控哪些片区由一个长度为 $m$ 的二进制字符串描述，字符串中第 $i$ 位为 $'1'$ 表示该摄像头能监控第 $i$ 个片区，否则不能监控。由于监控室大屏幕一次最多只能展示 $8$ 个摄像头画面，所以需要从摄像头中选取一个子集（至少一个、至多 $8$ 个），使得这些摄像头合起来监控的片区数量最多。若多个选法能达到最大监控片区数量，则统计方案数（注意：同一片区被多个摄像头监控只计一次）。

---

## 解题思路

- **状态表示**  
  每个摄像头的监控区域可以用一个二进制串表示，我们可以将其转换为一个位集（例如 C++ 中的 `bitset`、Python 中用整数保存二进制信息、Java 中的 `BitSet`）。

- **枚举子集**  
  因为一次最多选取 $8$ 个摄像头，所以只需要枚举所有大小在 $1$ 到 $8$ 之间的摄像头组合。由于 $n \le 25$，枚举所有组合总数为  
  $$\sum_{k=1}^{8} C(n,k)$$  
  即使最坏情况也在 $1.8$ 百万级别，枚举是可行的。

- **计算覆盖片区数**  
  对于每个组合，利用位运算将各摄像头监控的区域做“或”运算，计算“或”运算结果中 $'1'$ 的个数即为该组合能监控的片区数。

- **更新答案**  
  遍历所有组合，记录最大的监控片区数以及达到该数目的组合方案数。

---

## 代码分析

- **递归枚举**  
  利用递归或迭代枚举所有选取方案，对于每个方案计算当前的联合监控区域。

- **位运算优化**  
  使用位运算（如 C++ 的 `bitset`、Python 的整数位运算、Java 的 `BitSet`）高效地合并各摄像头的监控区域。

- **时间复杂度**  
  枚举所有组合的时间复杂度为  
  $$O\Bigl(\sum_{k=1}^{8} C(n,k)\Bigr)$$  
  对于每个组合合并 $m$ 个片区信息（位运算）开销可忽略，总体可以接受。

- **问题本质**  
  本题考察的是枚举组合与利用位运算进行集合合并的技巧。核心在于如何利用每个摄像头的监控信息，通过组合“或”运算得到联合覆盖区域，再统计 $'1'$ 的个数，从而解决最大覆盖与方案计数问题。

---

## C++ 

```cpp
#include <iostream>
#include <vector>
#include <bitset>
#include <functional>
using namespace std;

int main(){
    int n, m;
    cin >> n >> m;
    // 定义一个bitset数组，存储每个摄像头监控的片区信息
    vector<bitset<128>> cams(n);
    for (int i = 0; i < n; i++){
        string s;
        cin >> s;
        // 将字符串转换为bitset，若第j位为'1'则设置该位
        for (int j = 0; j < m; j++){
            if(s[j]=='1'){
                cams[i].set(j);
            }
        }
    }
    
    int maxCoverage = 0;         // 最大监控的片区数
    long long ways = 0;          // 达到最大监控片区数的方案数
    
    // 递归枚举选取的摄像头组合
    // 参数：当前摄像头起始下标、已选个数、当前联合监控区域
    function<void(int, int, bitset<128>&)> dfs = [&](int start, int count, bitset<128> &cur) {
        // 如果至少选择了一个摄像头，就更新答案
        if(count > 0){
            int cov = cur.count();
            if(cov > maxCoverage){
                maxCoverage = cov;
                ways = 1;
            } else if(cov == maxCoverage){
                ways++;
            }
        }
        // 当已选数量达到8个时，不能继续选取
        if(count == 8) return;
        // 枚举剩余摄像头
        for (int i = start; i < n; i++){
            bitset<128> next = cur | cams[i]; // 将当前监控区域与摄像头i的区域取或
            dfs(i + 1, count + 1, next);
        }
    };
    
    bitset<128> empty; // 空的监控区域
    dfs(0, 0, empty);
    
    cout << maxCoverage << " " << ways << endl;
    return 0;
}
```
## Python 

```python
import sys
import itertools

def main():
    # 读取输入
    input_line = sys.stdin.readline().strip()
    if not input_line:
        return
    n, m = map(int, input_line.split())
    cams = []
    for _ in range(n):
        s = sys.stdin.readline().strip()
        # 将字符串转换为整数表示位图，'1'的位置对应1
        cam = int(s, 2)
        cams.append(cam)
    
    maxCoverage = 0  # 最大监控的片区数
    ways = 0       # 达到最大监控片区数的方案数

    # 枚举选取1到8个摄像头的所有组合
    for k in range(1, min(n, 8) + 1):
        # itertools.combinations生成所有下标为k的组合
        for comb in itertools.combinations(range(n), k):
            union = 0
            # 计算组合中所有摄像头监控区域的“或”
            for idx in comb:
                union |= cams[idx]
            # 计算监控到的片区数量：统计二进制中1的个数
            cov = bin(union).count('1')
            if cov > maxCoverage:
                maxCoverage = cov
                ways = 1
            elif cov == maxCoverage:
                ways += 1
    print(maxCoverage, ways)

if __name__ == '__main__':
    main()
```
## Java

```java
import java.util.*;
import java.io.*;
public class Main {
    public static void main(String[] args) throws Exception {
        // 输入读取
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] parts = br.readLine().trim().split("\\s+");
        int n = Integer.parseInt(parts[0]);
        int m = Integer.parseInt(parts[1]);
        
        // 用BitSet数组存储每个摄像头监控的片区信息
        BitSet[] cams = new BitSet[n];
        for (int i = 0; i < n; i++){
            String s = br.readLine().trim();
            cams[i] = new BitSet(m);
            for (int j = 0; j < m; j++){
                if (s.charAt(j) == '1'){
                    cams[i].set(j);
                }
            }
        }
        
        // 全局变量，记录最大监控片区数以及对应方案数
        int[] maxCoverage = new int[]{0};
        long[] ways = new long[]{0};
        
        // 递归枚举选取的摄像头组合
        // 参数：起始下标、已选个数、当前联合监控区域
        dfs(0, 0, new BitSet(m), n, m, cams, maxCoverage, ways);
        
        // 输出答案
        System.out.println(maxCoverage[0] + " " + ways[0]);
    }
    
    // 递归函数，枚举组合
    public static void dfs(int start, int count, BitSet cur, int n, int m, BitSet[] cams, int[] maxCoverage, long[] ways){
        if(count > 0){
            // 计算当前联合监控区域中1的个数
            int cov = cur.cardinality();
            if(cov > maxCoverage[0]){
                maxCoverage[0] = cov;
                ways[0] = 1;
            } else if(cov == maxCoverage[0]){
                ways[0]++;
            }
        }
        if(count == 8) return; // 选满8个摄像头则返回
        for (int i = start; i < n; i++){
            // 复制当前的BitSet，并将摄像头i的区域合并
            BitSet next = (BitSet)cur.clone();
            next.or(cams[i]);
            dfs(i + 1, count + 1, next, n, m, cams, maxCoverage, ways);
        }
    }
}
```