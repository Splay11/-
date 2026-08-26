# 思路
统计 c0 为偶数的数量，c1 为奇数的数量，m = n / 2
- c0 == c1，答案为 0
- c0 < c1，选择 (c1 - m) 个奇数均进行一次乘2操作变成偶数，任选 (c1 - m) 个奇数即可
- c0 > c1，选择 (c0 - m) 个偶数进行下取整除法变成奇数，一定可以变成奇数，最差就是变成 1 
  选择哪些偶数进行下取整呢？
  就是下取整除法从偶数变成奇数的最小次数的前 (c0 - m) 个偶数即可
  
时间复杂度：$O(n\log n)$

# 代码
### python
```python
n = int(input())
a = list(map(int, input().split()))
even2odd = []
cnt = [0, 0]

for i in range(n):
    v = a[i]
    cnt[v & 1] += 1
    c = 0
    while v % 2 == 0:
        c += 1
        v //= 2

    if c > 0:
        even2odd.append(c)

m = n // 2

if cnt[0] == cnt[1]:
    print(0)
elif cnt[0] > cnt[1]:
    even2odd.sort()
    need = cnt[0] - m
    ans = sum(even2odd[:need])
    print(ans)
else:
    print(m - cnt[0])
    
```
### java
```java
import java.util.*;

public class Main {

    public static void main(String[] args) {
        new Main().run();
    }

    public void run() {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] arr = new int[n];

        int odd = 0, even = 0;

        List<Integer> evenList = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            arr[i] = sc.nextInt();
            if (arr[i] % 2 != 0) odd++;
            else {
                even++;
                evenList.add(arr[i]);
            }
        }

        // 先统计初始数组的偶数和奇数的个数，然后再判断哪样是更少的操作
        int target = n / 2;   // 数组一半的个数
        if (target == odd) {
            System.out.println(0);
            return;
        }

        // 再考虑转化方案：
        /*
         * 如果是一个奇数，除 2 向下取整则得到偶数。如果奇数*2，则得到偶数
         * 如果是偶数，除 2，可能是变成奇数，比如 6/2 = 3；也可能是得到偶数。乘 2，也肯定是偶数
         */
        // 所以两者是可以相互转化的，看哪种情况更小

        int ans = 0;
        //1. 奇数转偶数，直接 ans = odd - target（因为只要 *2 即可）
        if (odd > even) {
            ans = odd - target;
        } else {
            // 2. 偶数转奇数，需要考虑拿出来能转为奇数的数中需要的操作次数最少的那几个,比如用一个数组记录所有偶数变成奇数的操作次数
            // 偶数一定能转为奇数，也就是 1
            List<Integer> ops = new ArrayList<>();
            for (int i = 0; i < even; i++) {
                int x = evenList.get(i);  // 拿到偶数
                ops.add(getOps(x));   // 存储操作次数
            }

            ops.sort((a, b) -> a - b);
            // 累积求和前 even - target 个数的操作次数
            for(int i = 0; i < even - target; i++){
                ans += ops.get(i);
            }
        }
        System.out.println(ans);
    }

    // 得到一个偶数转为奇数的次数
    public int getOps(int x) {
        int cnt = 0;
        while(x % 2 == 0){
            x /= 2;
            cnt++;
        }
        return cnt;
    }
}
```
### C++
```C++
#include<bits/stdc++.h>
using namespace std;

const int N = 1e5 + 10;
int n, cnt0, cnt1, st[N]; // st[i]表示将第i个偶数转成奇数的最少操作次数 
int main(){
	scanf("%d", &n);
	for(int i = 1, x; i <= n; i++){
		scanf("%d", &x);
		if(x&1) cnt1++; // 奇数个数+1
		else{
			 cnt0++; // 偶数个数+1 
			 for(int j = 31; j>=1; j--){
			 	// (x)&(-x)得到的是一个数的二进制表示的末尾1的对应值
				 // 比如：x=6,则的x的二进制表示为110,则(x)&(-x)=(110)&(010)= 010
				 // -6的二进制表示是对110先按位取反得到001，再加1得到010，即110 -> 001 -> 010 
			 	if(1<<j == (x&(-x))){
			 		st[cnt0] = j;
			 		break;
			 	}
			 }
		}
	}
	
	long long ans = 0;
	if(cnt0 == cnt1){ // 奇数个数和偶数个数一样多 
		ans = 0;		
	} else if(cnt0 < cnt1){ // 奇数个数多于偶数个数,只需要进行这样的操作：一个奇数乘以2,就可以得到偶数；重复这样的操作，直到奇数个数和偶数个数一样多 
		ans = (cnt1 - cnt0)/2;
	}else { // 奇数个数少于偶数个数,需要将若干偶数转成奇数；需要得到每个偶数转成奇数的最少操作数，然后按最少操作数进行升序排序，选择最小的若干个，直到奇数个数和偶数个数一样多 
		sort(st+1, st+1+cnt0);
		int num = (cnt0 - cnt1)/2; // num表示需要将偶数转变成奇数的个数 
		for(int i = 1; i <= num; i++){
			ans += st[i];
		}
	}
	printf("%lld\n", ans);
	return 0;
}
```