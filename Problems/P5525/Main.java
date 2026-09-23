import java.io.*;
import java.util.*;

public class Main {
    // 质因数分解，返回 [质数积, 指数列表]
    static Object[] factorize(long n) {
        long prod = 1;
        ArrayList<Integer> exps = new ArrayList<>();
        for (long d = 2; d * d <= n; d++) {
            if (n % d == 0) {
                prod *= d;
                int cnt = 0;
                while (n % d == 0) {
                    n /= d;
                    cnt++;
                }
                exps.add(cnt);
            }
        }
        if (n > 1) {
            prod *= n;
            exps.add(1);
        }
        return new Object[]{prod, exps};
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        long n = Long.parseLong(br.readLine().trim());
        if (n == 1) {
            System.out.println("1 0");
            return;
        }
        Object[] res = factorize(n);
        long mn = (Long) res[0];
        @SuppressWarnings("unchecked")
        ArrayList<Integer> exps = (ArrayList<Integer>) res[1];
        int maxE = 0;
        for (int e : exps) maxE = Math.max(maxE, e);
        // 找到 >= maxE 的最小 2 的幂
        long pw = 1;
        int k = 0;
        while (pw < maxE) {
            pw *= 2;
            k++;
        }
        boolean needMul = false;
        for (int e : exps) {
            if (e != pw) {
                needMul = true;
                break;
            }
        }
        int ops = k + (needMul ? 1 : 0);
        System.out.println(mn + " " + ops);
    }
}
