### 思路：思维题

要让字典序最大，同时符合条件，直接将$n$排列逆序输出即可。

题目不难，难在想到这个点。

时间复杂度：$O(N)$

c++
```cpp
#include <iostream>
#include <cstdio>
using namespace std;
int n;

int main(){
	cin>>n;
	for(int i=n;i;--i){
		cout<<i<<" ";
	}
	
	return 0;
}
```
java
```java
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        
        for (int i = n; i > 0; i--) {
            System.out.print(i + " ");
        }
        
        scanner.close();
    }
}
```

python
```python
n = int(input())

for i in reversed(range(1, n + 1)):
    print(i, end = ' ')
```