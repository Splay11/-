## 题目思路

除了1以外，一个大于0的整数要么是质数要么是合数，所以只需要计算集合的元素数量即可。如果数组包含1，则减去一个元素。

## 代码

**Java**

~~~java
import java.util.HashSet;
import java.util.Scanner;
import java.util.Set;

public class UniqueIntegers {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        int n = scanner.nextInt();
        Set<Integer> sett = new HashSet<>();
        for (int i = 0; i < n; i++) {
            int value = scanner.nextInt();
            sett.add(value);
        }

        int count = sett.size();
        if (sett.contains(1)) {
            count -= 1;
        }

        System.out.println(count);
    }
}

~~~

**C++**

~~~c++
#include <iostream>
#include <set>

using namespace std;

int main() {
    int n;
    cin >> n;
    
    set<int> sett;
    for (int i = 0; i < n; i++) {
        int value;
        cin >> value;
        sett.insert(value);
    }
    
    int count = sett.size();
    if (sett.find(1) != sett.end()) {
        count--;
    }

    cout << count << endl;
    
    return 0;
}

~~~

**Python**

~~~python
n = int(input())
a = list(map(int, input().split()))
sett = set(a)
print(len(sett) - (1 if 1 in sett else 0))
~~~


**会员可通过查看《已通过》的提交记录来查看其他语言哦~**