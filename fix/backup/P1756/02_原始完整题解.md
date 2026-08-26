# 思路
模拟题，根据题意进行贪心模拟即可。
我们需要将所有非 1 的字符全部修改为 1 ，所以一旦遇到一个为 1 的字符，就将其修改为 1 ，并将其相邻的字符也一并修改为 1。
这里我们考虑将当前字符以及其右边的字符修改为 1 的贪心方式，这样遍历的同时进行修改，使得最终需要进行修改的字符数量最少即可。
时间复杂度：$O(nm)$

# 代码
### python
```python
n, m = map(int, input().split())
s = []
for i in range(n):
    s.append(list(input()))

ans = 0
for i in range(n):
    for j in range(m):
        if s[i][j] == '0':
            ans += 1
            s[i][j] = '1'
            if j + 1 < m:
                s[i][j + 1] = '1'

print(ans)
```
### java
```java
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int m = sc.nextInt();
        char[][] words = new char[n][m];
        for (int i = 0; i < n; i++) {
            String str = sc.next();
            char[] w = str.toCharArray();
            words[i] = w;
        }
        int ans = change(words,n,m);
        System.out.println(ans);
    }

    private static int change(char[][] words, int n, int m) {
        int ans = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                if(words[i][j] == '0'){
                    if(j < m-1){
                        words[i][j] = '1';
                        words[i][j+1] = '1';
                    }else{
                        words[i][j] = '1';
                    }
                    ans++;
                }
            }
        }
        return ans;
    }
}
```
### C++
```C++
#include <iostream>
#include <vector>

using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    
    vector<string> matrix(n);
    for (int i = 0; i < n; i++) {
        cin >> matrix[i];
    }

    int operations = 0;

    // 遍历每一行
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            // 如果当前字符是0，进行操作
            if (matrix[i][j] == '0') {
                operations++; // 记录一次操作
                
                // 将1*2区域的字符变为1
                if (j + 1 < m) {
                    matrix[i][j] = '1'; // 当前字符变为1
                    matrix[i][j + 1] = '1'; // 右侧字符变为1
                } else {
                    matrix[i][j] = '1'; // 如果是最后一列，则只变当前字符
                }
            }
        }
    }

    cout << operations << endl;
    return 0;
}
```