import java.util.ArrayList;
import java.util.Arrays;
import java.util.BitSet;
import java.util.Scanner;

public class Main {
    static final int CAP = 10000;
    static final int NEED = 4;

    static ArrayList<Integer> pickFour(int[] b, int[] w) {
        int n = b.length;
        if (n < NEED) {
            return null;
        }
        Integer[] order = new Integer[n];
        for (int i = 0; i < n; i++) {
            order[i] = i;
        }
        // 按编号从小到大，保证后面贪心得到字典序最小的一组
        Arrays.sort(order, (i, j) -> Integer.compare(b[i], b[j]));
        int[] bb = new int[n];
        int[] ww = new int[n];
        for (int i = 0; i < n; i++) {
            bb[i] = b[order[i]];
            ww[i] = w[order[i]];
        }

        // suffix[i][k]：从下标 i 到末尾恰好选 k 件能凑出的总价
        BitSet[][] suffix = new BitSet[n + 1][NEED + 1];
        for (int i = 0; i <= n; i++) {
            for (int k = 0; k <= NEED; k++) {
                suffix[i][k] = new BitSet(CAP + 1);
            }
        }
        suffix[n][0].set(0);
        for (int i = n - 1; i >= 0; i--) {
            for (int k = 0; k <= NEED; k++) {
                suffix[i][k] = (BitSet) suffix[i + 1][k].clone();
            }
            for (int k = NEED - 1; k >= 0; k--) {
                // dp[i][k][s]：从 i 往后恰好选 k 件，总价能否为 s
                // clone 后缀是不选第 i 件，继承 dp[i+1][k]
                // 左移 w[i] 再或上去，是选第 i 件、总价加上售价
                // k 从大到小，保证每件最多用一次
                suffix[i][k + 1].or(shiftLeft(suffix[i + 1][k], ww[i]));
            }
        }
        if (suffix[0][NEED].isEmpty()) {
            return null;
        }
        int remainS = suffix[0][NEED].previousSetBit(CAP);
        int remainK = NEED;
        ArrayList<Integer> ans = new ArrayList<>();
        for (int i = 0; i < n && remainK > 0; i++) {
            int ns = remainS - ww[i];
            int nk = remainK - 1;
            // 判断 dp[i+1][nk][ns] 是否可行：选完当前件后后缀还能不能凑齐
            // 编号已升序，能选就选，得到字典序最小方案
            if (ns >= 0 && suffix[i + 1][nk].get(ns)) {
                ans.add(bb[i]);
                remainS = ns;
                remainK = nk;
            }
        }
        return ans;
    }

    // 把位集整体左移 sh 位，超过 CAP 的位丢掉
    static BitSet shiftLeft(BitSet src, int sh) {
        BitSet dst = new BitSet(CAP + 1);
        for (int s = src.nextSetBit(0); s >= 0; s = src.nextSetBit(s + 1)) {
            if (s + sh <= CAP) {
                dst.set(s + sh);
            }
        }
        return dst;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int m = sc.nextInt();
        int[] b = new int[m];
        int[] w = new int[m];
        for (int i = 0; i < m; i++) {
            b[i] = sc.nextInt();
            w[i] = sc.nextInt();
        }
        ArrayList<Integer> ans = pickFour(b, w);
        if (ans == null) {
            System.out.println(0);
        } else {
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < ans.size(); i++) {
                if (i > 0) {
                    sb.append(' ');
                }
                sb.append(ans.get(i));
            }
            System.out.println(sb.toString());
        }
        sc.close();
    }
}
