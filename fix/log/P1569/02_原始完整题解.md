## 思路
此题的要求是在一个排列中找到一个长度为k的连续字段也是一个排列，并且最多交换一次，这一个连续字段的排列不一定是顺序，也有可能是顺序的，我们知道一个长度为k的排列数字一定是从1到k，在这一整个大排列中1到k也只会出现一次，那么我们就可以针对1到k的数出现的位置做考虑，先将1到k的数出现的位置记录下来并且排序，若是相邻的出现位置相差均为1，那么显然这k个数都是相邻的。

若是交换一次才能使所有位置相邻，那么便找到第一个不相邻的位置，这个位置是要交换的，另一个位置一定在出现位置最后或最前，当然前提是假设通过一次交换可以使所有位置相邻，所以可以通过检查前k-1个数出现的位置和后k-1个数是否只缺少1个位置使之连续来判断，具体请看代码，若是这两个条件均不能满足那么就无法通过1次交换使之连续。
## 代码


### java

```java
import java.util.*;

public class Main {
    static int x = -1, n;
    static Scanner sc = new Scanner(System.in);
    public static void main(String[] args) {
        n = sc.nextInt();
        int k = sc.nextInt(), idx = 0;
        int[] a = new int[k];
        for (int i = 0; i < n; i++) {
            int t = sc.nextInt();
            if (t <= k) {
                a[idx++] = i + 1;
            }
        }
        Arrays.sort(a);
        
        if (isContinuous(a)) {
            System.out.println("YES\n0");
        } else if (check(a, 0, a.length - 2)) {
            System.out.println("YES\n1");
            System.out.println(x + " " + a[a.length - 1]);
        } else if (check(a, 1, a.length - 1)) {
            System.out.println("YES\n1");
            System.out.println(a[0] + " " + x);
        } else {
            System.out.println("NO");
        }
    }
    static boolean isContinuous(int[] positions) {
        return positions[positions.length - 1] - positions[0] + 1 == positions.length;
    }
    static boolean check(int[] a, int L, int R) {
        if (a[L] == 1)
            x = a[R] + 1;
        else
            x = a[L] - 1;
        for (int i = L + 1; i <= R; i++) {
            if (a[i] != a[i - 1] + 1) {
                x = a[i] - 1;
            }
        }
        return a[R] - a[L] <= a.length - 1;
    }
}
/*


 */
```