## 题目思路

考虑暴力枚举，第一个技能如果释放，肯定应该先于第二个技能，这样效果至少不差甚至更优

可以排序后枚举每一个怪物的血量，使用第一个技能让当前怪物血量死亡（其前面的怪物也肯定死亡，血量都比这个怪物少），后面的怪物都使用第二个技能，最终得出的最小花费就是答案。

时间复杂度$O(nlogn)$

## 代码

**Java**

~~~java
import java.util.Arrays;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int[] a = new int[n];

        for (int i = 0; i < n; ++i) {
            a[i] = scanner.nextInt();
        }

        Arrays.sort(a);
        int ans = n * 2 + 1;
        for (int i = 0; i < n; ++i) {
            ans = Math.min(ans, a[i] + (n - i - 1) * 2);
        }

        System.out.println(ans);
    }
}

~~~

**C++**

~~~c++
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);

    for (int i = 0; i < n; ++i) {
        cin >> a[i];
    }

    sort(a.begin(), a.end());
    int ans = n * 2 + 1;
    for (int i = 0; i < n; ++i) {
        ans = min(ans, a[i] + (n - i - 1) * 2);
    }

    cout << ans << endl;

    return 0;
}
~~~

**Python**

~~~python
n = int(input())
a = list(map(int, input().split()))

a.sort()
ans = n * 2 + 1
for i in range(n):
    ans = min(ans, a[i] + (n - i - 1) * 2)

print(ans)

~~~

**会员可通过查看《已通过》的提交记录来查看其他语言哦~**