import java.util.Scanner;

public class Main {
    static final long NEG = -1000000000000000000L;

    static long maxValue(int h, int w, int[][] v) {
        // 走了 t 步后：A 在 (t-c1, c1)，B 在 (t-(w-1-c2), c2)
        int endT = h + w - 2;
        long[][] dp = new long[w][w];
        long[][] ndp = new long[w][w];
        for (int i = 0; i < w; i++) {
            for (int j = 0; j < w; j++) {
                dp[i][j] = NEG;
            }
        }
        // 起点不同（w>=3），把两个起点的价值都算上
        dp[0][w - 1] = (long) v[0][0] + v[0][w - 1];
        for (int t = 0; t < endT; t++) {
            for (int c1 = 0; c1 < w; c1++) {
                for (int c2 = 0; c2 < w; c2++) {
                    ndp[c1][c2] = NEG;
                }
            }
            for (int c1 = 0; c1 < w; c1++) {
                for (int c2 = 0; c2 < w; c2++) {
                    long cur = dp[c1][c2];
                    if (cur == NEG) {
                        continue;
                    }
                    int r1 = t - c1;
                    int r2 = t - (w - 1 - c2);
                    if (r1 < 0 || r1 >= h || r2 < 0 || r2 >= h) {
                        continue;
                    }
                    int[] ar = new int[2];
                    int[] ac = new int[2];
                    int an = 0;
                    // A：向下或向右
                    if (r1 + 1 < h) {
                        ar[an] = r1 + 1;
                        ac[an] = c1;
                        an++;
                    }
                    if (c1 + 1 < w) {
                        ar[an] = r1;
                        ac[an] = c1 + 1;
                        an++;
                    }
                    int[] br = new int[2];
                    int[] bc = new int[2];
                    int bn = 0;
                    // B：向下或向左
                    if (r2 + 1 < h) {
                        br[bn] = r2 + 1;
                        bc[bn] = c2;
                        bn++;
                    }
                    if (c2 - 1 >= 0) {
                        br[bn] = r2;
                        bc[bn] = c2 - 1;
                        bn++;
                    }
                    for (int i = 0; i < an; i++) {
                        for (int j = 0; j < bn; j++) {
                            int nr1 = ar[i], nc1 = ac[i];
                            int nr2 = br[j], nc2 = bc[j];
                            // 同一时刻不能站在同一格
                            if (nr1 == nr2 && nc1 == nc2) {
                                continue;
                            }
                            long val = cur + v[nr1][nc1] + v[nr2][nc2];
                            if (val > ndp[nc1][nc2]) {
                                ndp[nc1][nc2] = val;
                            }
                        }
                    }
                }
            }
            long[][] tmp = dp;
            dp = ndp;
            ndp = tmp;
        }
        return dp[w - 1][0];
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int h = sc.nextInt();
        int w = sc.nextInt();
        int[][] v = new int[h][w];
        for (int i = 0; i < h; i++) {
            for (int j = 0; j < w; j++) {
                v[i][j] = sc.nextInt();
            }
        }
        System.out.println(maxValue(h, w, v));
        sc.close();
    }
}
