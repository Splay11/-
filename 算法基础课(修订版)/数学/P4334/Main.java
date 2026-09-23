import java.io.*;
import java.util.*;

/*
  说明：
  - 使用 long 保证在 1e9 范围内的 lcm 乘积 (<=1e18) 不溢出。
  - 因子枚举为 O(sqrt(v))，对 x 与 y 各做一次，整体足够快。
*/
public class Main {
    static long gcd(long a, long b) {
        while (b != 0) {
            long t = a % b;
            a = b;
            b = t;
        }
        return a;
    }

    static ArrayList<Long> divisorsLeq(long v, long n) {
        ArrayList<Long> res = new ArrayList<>();
        for (long i = 1; i * i <= v; ++i) {
            if (v % i == 0) {
                if (i <= n) res.add(i);
                long j = v / i;
                if (j != i && j <= n) res.add(j);
            }
        }
        return res;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] sp = br.readLine().trim().split("\\s+");
        long n = Long.parseLong(sp[0]);
        long x = Long.parseLong(sp[1]);
        long y = Long.parseLong(sp[2]);

        // 计算 |A ∪ B|
        long g = gcd(x, y);
        long lcm = (x / g) * y; // 在约束内不溢出
        long M = n / x + n / y - n / lcm;

        // 因子集合（不超过 n），去重
        HashSet<Long> S = new HashSet<>();
        for (long d : divisorsLeq(x, n)) S.add(d);
        for (long d : divisorsLeq(y, n)) S.add(d);

        // 统计需要额外补计的因子
        long extra = 0;
        for (long d : S) {
            if (d % x != 0 && d % y != 0) ++extra;
        }

        System.out.println(M + extra);
    }
}
