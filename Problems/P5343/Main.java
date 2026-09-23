import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Main {
    static final int MOD = 1000000007;

    static long pathSum(long p) {
        // S(p) = sum_{j=1}^{p} 2^{ctz(j)}
        // i ⊕ (i+1) = 2^{ctz(i+1)+1} - 1，故答案为 2*S(p) - p - 1
        long s = 0;
        for (int k = 0; k <= 60; k++) {
            long pk = 1L << k;
            if (pk > p) {
                break;
            }
            // ctz = k 的个数是 floor(p/2^k) - floor(p/2^{k+1})
            long diff = (p >>> k) - (p >>> (k + 1));
            s += pk % MOD * (diff % MOD) % MOD;
            if (s >= MOD) {
                s -= MOD;
            }
        }
        long ans = (2 * s % MOD - p % MOD - 1) % MOD;
        if (ans < 0) {
            ans += MOD;
        }
        return ans;
    }

    static List<Long> solveAll(List<Long> ps) {
        List<Long> res = new ArrayList<Long>();
        for (int i = 0; i < ps.size(); i++) {
            res.add(pathSum(ps.get(i)));
        }
        return res;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int q = sc.nextInt();
        List<Long> ps = new ArrayList<Long>();
        for (int i = 0; i < q; i++) {
            ps.add(sc.nextLong());
        }
        List<Long> ans = solveAll(ps);
        for (int i = 0; i < ans.size(); i++) {
            System.out.println(ans.get(i));
        }
        sc.close();
    }
}
