## 题目思路

考虑使用map维护a[i] + b[i]相等的数量cnt，对于每一种互补的所有下标，其可以产生的对应的子序列数量等于$2^{cnt} -1$种，即排除一个元素都不选的剩余情况。

时间复杂度O(nlogn)

## 代码

**Java**

~~~java
import java.util.*;

public class Main {
    static final int mod = 1_000_000_007;

    public static int qmi(int x, int k) {
        int res = 1;
        while (k > 0) {
            if ((k & 1) == 1) {
                res = (int)((long)res * x % mod);
            }
            x = (int)((long)x * x % mod);
            k >>= 1;
        }
        return res;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int[] a = new int[n];
        int[] b = new int[n];

        for (int i = 0; i < n; ++i) {
            a[i] = scanner.nextInt();
        }

        for (int i = 0; i < n; ++i) {
            b[i] = scanner.nextInt();
        }

        Map<Integer, Integer> mapp = new HashMap<>();
        for (int i = 0; i < n; ++i) {
            int key = a[i] + b[i];
            mapp.put(key, mapp.getOrDefault(key, 0) + 1);
        }

        long ans = 0;
        for (int val : mapp.values()) {
            ans +=  (qmi(2, val) - 1 + mod) % mod;
        }

        System.out.println(ans % mod);
    }
}

~~~

**C++**

~~~c++
#include <iostream>
#include <vector>
#include <unordered_map>

using namespace std;

const int mod = 1e9 + 7;

int qmi(int x, int k) {
    int res = 1;
    while (k) {
        if (k & 1) {
            res = (long long)res * x % mod;
        }
        x = (long long)x * x % mod;
        k >>= 1;
    }
    return res;
}

int main() {
    int n;
    cin >> n;
    vector<int> a(n), b(n);

    for (int i = 0; i < n; ++i) {
        cin >> a[i];
    }

    for (int i = 0; i < n; ++i) {
        cin >> b[i];
    }

    unordered_map<int, int> mapp;
    for (int i = 0; i < n; ++i) {
        mapp[a[i] + b[i]]++;
    }

    long long ans = 0;
    for (auto it : mapp) {
        ans += (qmi(2, it.second) - 1 + mod) % mod;
    }

    cout << ans % mod << endl;

    return 0;
}


~~~

**Python**

~~~python
n = int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))
mapp = {}
for x, y in zip(a, b):
    mapp[x + y] = mapp.get(x + y, 0) + 1
mod = int(1e9 + 7)
def qmi(x, k):
    res = 1
    while k:
        if k & 1:
            res = res * x % mod
        x = x * x % mod
        k >>= 1
    return res
ans = 0
for y in mapp.values():
    ans += (qmi(2, y) - 1 + mod) % mod
print(ans % mod)

~~~

**会员可通过查看《已通过》的提交记录来查看其他语言哦~**