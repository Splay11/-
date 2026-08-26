### 思路：模拟

直接按照题意模拟即可。

时间复杂度$O(N)$

c++
```cpp

#include <iostream>
#include <cstdio>
using namespace std;

int n,k;
string s;

int main(){
	cin>>n>>k;
	cin>>s;
	for(int i=1;i<s.length();i++){
		k-=s[i]-s[i-1];
		if(k<0) break;
	}
	if(k<0) cout<<-1;
	else cout<<k;
	
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
        int k = scanner.nextInt();
        scanner.nextLine();
        String s = scanner.nextLine();
        
        for (int i = 1; i < s.length(); i++) {
            k -= s.charAt(i) - s.charAt(i - 1);
            if (k < 0) {
                break;
            }
        }
        
        if (k < 0) {
            System.out.println(-1);
        } else {
            System.out.println(k);
        }
    }
}
```

python
```python
n, k = input().strip().split(" ")
n = int(n)
s = input()
k = int(k)

for i in range(1, len(s)):
    k -= int(ord(s[i]) - ord(s[i - 1]))
    if k < 0:
        break

if k < 0:
    print(-1)
else:
    print(k)
```