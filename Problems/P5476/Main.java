import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.StringTokenizer;

public class Main {
    static final int MAXB = 1000000;

    // 线性筛最小质因子，后面拆指纹用
    static int[] buildSpf() {
        int[] spf = new int[MAXB + 1];
        for (int i = 0; i <= MAXB; i++) {
            spf[i] = i;
        }
        for (int i = 2; i * (long) i <= MAXB; i++) {
            if (spf[i] == i) {
                for (int j = i * i; j <= MAXB; j += i) {
                    if (spf[j] == j) {
                        spf[j] = i;
                    }
                }
            }
        }
        return spf;
    }

    static long countPairs(int[] vals) {
        int[] spf = buildSpf();
        long cnt1 = 0;
        long special = 0;
        Map<Integer, Long> primeCnt = new HashMap<Integer, Long>();
        Map<Integer, Long> squareCnt = new HashMap<Integer, Long>();
        for (int t = 0; t < vals.length; t++) {
            int x = vals[t];
            if (x == 1) {
                // 1 只能和 p^3 或 p*q 配对
                cnt1++;
                continue;
            }
            int n = x;
            ArrayList<int[]> factors = new ArrayList<int[]>();
            while (n > 1) {
                int p = spf[n];
                int c = 0;
                while (n % p == 0) {
                    n /= p;
                    c++;
                }
                factors.add(new int[] {p, c});
            }
            if (factors.size() == 1) {
                int p = factors.get(0)[0];
                int c = factors.get(0)[1];
                if (c == 1) {
                    Long old = primeCnt.get(p);
                    primeCnt.put(p, old == null ? 1L : old + 1);
                } else if (c == 2) {
                    Long old = squareCnt.get(p);
                    squareCnt.put(p, old == null ? 1L : old + 1);
                } else if (c == 3) {
                    special++;
                }
            } else if (factors.size() == 2 && factors.get(0)[1] == 1 && factors.get(1)[1] == 1) {
                // 两个不同质数之积
                special++;
            }
        }
        // 1 与「恰好四因子」的数
        long ans = cnt1 * special;
        long totalP = 0;
        for (Map.Entry<Integer, Long> e : primeCnt.entrySet()) {
            long c = e.getValue();
            totalP += c;
            // 同一个质数两次乘起来是平方，因子个数不是 4
            ans -= c * (c - 1) / 2;
            Long sq = squareCnt.get(e.getKey());
            if (sq != null) {
                // p 与 p^2 乘积是 p^3
                ans += c * sq;
            }
        }
        // 不同质数两两配对
        ans += totalP * (totalP - 1) / 2;
        return ans;
    }

    public static void main(String[] args) throws IOException {
        // 单行最长约 1e5 个数，用 BufferedReader
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int m = Integer.parseInt(st.nextToken());
        int[] vals = new int[m];
        for (int i = 0; i < m; i++) {
            vals[i] = Integer.parseInt(st.nextToken());
        }
        System.out.println(countPairs(vals));
    }
}
