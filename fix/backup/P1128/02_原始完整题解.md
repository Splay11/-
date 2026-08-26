计算一下待测答案有多少个在标准答案出现过即可。根据大小关系比就行。

C++
```c++
#include<bits/stdc++.h>
using namespace std;
const int maxn = 1e5 +5;
string a[maxn] , b[maxn];
int main (){
    int n;
    cin >> n;
    for (int i = 1 ; i <= n ; i++){
        cin >> b[i];
    }
    for (int i = 1 ; i <= n ; i++){
        cin >> a[i];
    }
    int ans = 0;
    for (int i = 1 ; i <= n ; i++){
        int cnt = 0;
        // 枚举待测答案的每个字符
        for (auto x : b[i]){
            // 看他在不在标准答案里
            for (auto y : a[i]){
                if (x == y){
                    cnt++;
                    break;
                }
            }
        }
        // 如果全部出现
        if (cnt == b[i].size()){
            // 部分
            if (a[i].size() > b[i].size()) ans += 1;
            // 全对
            else ans += 3;
        }
        // 如果没全部出现，肯定就是错的
    }
    cout << ans << endl;
    return 0;
}
```

Java

```java
import java.util.*;

public class Main {
    
	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();

        String[] a = new String[n]; // 作答
        String[] b = new String[n]; // 标准答案
        for (int i = 0; i < n; i++) {
            a[i] = sc.next();
        }
        for (int i = 0; i < n; i++) {
            b[i] = sc.next();
        }
        int res = 0;
        for (int i = 0; i < n; i++) {
            int count = 0;
            // 遍历“标准答案”中的每一个字符
            for (char x : a[i].toCharArray()) {
                // 看它是否在“作答”中出现
                for (char y : b[i].toCharArray()) {
                    if (x == y) {
                        count++;
                        break;
                    }
                }
            }
            // 如果“标准答案”的所有字符都在“作答”中出现
            if (count == a[i].length()) {
                if (b[i].length() <= a[i].length()) {   // 如果“标准答案”长度等于“作答”长度，则算全部正确，得 3 分
                    res += 3;
                } else {                                // 否则算作部分正确，得 1 分
                    res += 1;
                }
            }
            // 如果“标准答案”有一个字符在“作答”中未出现，则算作错误，不加分
        }
        System.out.println(res);
	}
}
```

Pythoon
```pythoon
n = int(input())
x = list(input().split())
y = list(input().split())
score = 0
for i in range(n):
    if x[i] == y[i]:
        score += 3
    else:
        flag = 1
        for a in x[i]:
            if a not in y[i]:
                flag = 0
                break
        if flag == 1:
            score += 1
print(score)

```