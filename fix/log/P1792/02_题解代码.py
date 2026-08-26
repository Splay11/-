## 题目思路

考虑贪心，将每个强化石的最大值的二进制位统计一下，即记录二进制每一位在该位置上是1的石头数量。

从大到小考虑位，如果该位置有石头，那肯定至少得用到这个位（不用，后面全部位置加起来也没用了大，比如$2^3>2^2+2^1+2^0$）。

当这个位置有两个以上的石头，那后面的位数都可以是1，道理同上。所以能放就放，有多后面就都可以置为1。

## 代码

**Java**

~~~java
import java.util.Scanner;

class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int T = scanner.nextInt();
        for (int t = 0; t < T; t++) {
            solve(scanner);
        }
    }

    static void solve(Scanner scanner) {
        int n = scanner.nextInt();
        int[] cnt = new int[31];
        for (int i = 0; i < n; ++i) {
            int x = scanner.nextInt();
            for (int j = 0; j < 31; ++j) {
                if ((x >> j & 1) == 1) {
                    cnt[j]++;
                }
            }
        }
        int ans = 0;
        for (int i = 30; i >= 0; --i) {
            if (cnt[i] > 0) {
                ans |= 1 << i;
                cnt[i]--;
            }
            if (cnt[i] > 0) {
                ans |= (1 << i) - 1;
                break;
            }
        }
        System.out.println(ans);
    }
}

~~~

**C++**

~~~c++
#include<bits/stdc++.h>

using namespace std;

typedef long long LL;
#define x first
#define y second
#define endl '\n'
const int fastio = []() {
    cin.tie(0)->sync_with_stdio(false);
    return 0;
}();

void solve() {
	int n;
	cin >> n;
	vector<int> cnt(31, 0);
	for (int i = 0, x;i < n;++ i) {
		cin >> x;
		for (int j = 0;j < 31;++ j) if (x >> j & 1) {
			++ cnt[j];
		}
	}
	int ans = 0;
	for (int i = 30; i>=0; -- i) {
		if (cnt[i]) {
			ans |= 1 << i;
			-- cnt[i];
		}	
		if (cnt[i]) {
			ans |= (1<<i) - 1;
			break;
		}
	}
	cout << ans << endl;
}

signed main() {
	int T = 1;
	cin >> T;
	while(T --) {
		solve();
	}
}
~~~

**Python**

~~~python
def solve():
    n = int(input())
    cnt = [0] * 31
    a = list(map(int, input().split(' ')))
    for x in a:
        for j in range(31):
            if x >> j & 1:
                cnt[j] += 1
    ans = 0
    for i in range(30, -1, -1):
        if cnt[i]:
            ans |= 1 << i
            cnt[i] -= 1
        if cnt[i]:
            ans |= (1 << i) - 1
            break
    print(ans)

T = int(input())
for _ in range(T):
    solve()


~~~

**会员可通过查看《已通过》的提交记录来查看其他语言哦~**