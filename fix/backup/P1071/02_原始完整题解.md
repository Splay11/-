## 思路

排列其实就是一个数组$n$个数，包好$1$到$n$各一位。所以我们可以将数组排序，将数组排序后，我们会得到一个$1$到$n$的数组，同时我们用$pos[i]$表示一个数$i$在原数组的位置。

我们拿样例$[2,1,5,3,4]$来讲解。

那么我们得到的$pos$数组是$[2,1,4,5,3]$。

我们将数字和$pos$绑定为二元组。所以原数组为$[(2,1),(1,2),(5,3),(3,4),(4,5)]$（二元组第一位表示数字，第二位表示位置）。我们排序后，数组变为$[(1,2),(2,1),(3,4),(4,5),(5,3)]$。

我们枚举排序数组，假设枚举到$i$，那么我们发现$[1,i]$的数组的数字其实是可以组成排列的，因为数组已经排序过了。但是它们的位置可能不相连。比如我们发现$i=2$时，是可以组成相连的排列的。但是$i=3$时，就不行，因为数字$3$的位置在$4$，而前面两位一个在$2$，一个在$1$。然后我们继续枚举$i$，发现$i=4$也不行，$i=5$时可以了，因为可以组成$[1,5]$的连在一起的排列。

那如何快速知道$[1,i]$的排列连在一起呢。其实只要求出$max(pos_i)$和$min(pos_i)$，它们的$max(pos_i)-min(pos_i)+1$如果等于数字的个数，那么就表示连在一起。

## Java代码

```Java
import java.util.Arrays;
import java.util.Comparator;
import java.util.Scanner;

public class Main {
    static class TwoTuple{
        int a, b;
        public TwoTuple(int a, int b){//二元组
            this.a = a;
            this.b = b;
        }
    }
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);//输入
        int t = in.nextInt();
        while (t-- > 0){
            int n = in.nextInt();
            TwoTuple[] arr = new TwoTuple[n];
            for(int i = 0; i < n; i++){
                int num = in.nextInt();
                arr[i] = new TwoTuple(num, i);
            }
            Arrays.sort(arr, new Comparator<TwoTuple>() {//按数值排序
                @Override
                public int compare(TwoTuple o1, TwoTuple o2) {
                    return o1.a - o2.a;
                }
            });
            int maxn = -1, minn = (int)1e9;//位置差值
            int ans = 0;
            for(int i = 0; i < n; i++){
                minn = Math.min(arr[i].b, minn);
                maxn = Math.max(arr[i].b, maxn);
                if(maxn - minn <= i){//等于题目思路中的maxn-minn+1<=i+1
                    ans++;
                }
            }
            System.out.println(ans);
        }
    }
}
```

## C++代码

```C++
#include <bits/stdc++.h>
using namespace std;
const int MAXN = 2e5 + 5;
typedef pair<int, int>pii;
int n;
pii arr[MAXN];
int main(){
	int t;
	cin >> t;
	while(t--){
		cin >> n;
		for(int i = 1; i <= n; i++){
			int num;
			cin >> num;
			arr[i] = {num, i};
		}
		sort(arr + 1, arr + n + 1);
		int minn = (int)1e9;
		int maxn = -1;
		int ans = 0;
		for(int i = 1; i <= n; i++){
			maxn = max(maxn, arr[i].second);
			minn = min(minn, arr[i].second);
			if(maxn - minn + 1 <= i)ans++;
		}
		cout << ans << endl;
	}
}
```