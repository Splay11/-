import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String a = br.readLine().trim();
        String b = br.readLine().trim();
        String c = br.readLine().trim();
        int n = a.length(), m = b.length(), p = c.length();

        // f[i][j][k]：后缀 LCS 长度
        int[][][] f = new int[n + 1][m + 1][p + 1];
        for (int i = n; i >= 0; i--) {
            for (int j = m; j >= 0; j--) {
                for (int k = p; k >= 0; k--) {
                    if (i == n || j == m || k == p) {
                        f[i][j][k] = 0;
                    } else if (a.charAt(i) == b.charAt(j) && b.charAt(j) == c.charAt(k)) {
                        f[i][j][k] = 1 + f[i + 1][j + 1][k + 1];
                    } else {
                        f[i][j][k] = Math.max(f[i + 1][j][k],
                                Math.max(f[i][j + 1][k], f[i][j][k + 1]));
                    }
                }
            }
        }

        int L = f[0][0][0];
        System.out.println(L);

        // 贪心按字典序构造
        int i = 0, j = 0, k = 0, remain = L;
        StringBuilder res = new StringBuilder();
        while (remain > 0) {
            for (char ch = 'a'; ch <= 'z'; ch++) {
                int ni = a.indexOf(ch, i);
                int nj = b.indexOf(ch, j);
                int nk = c.indexOf(ch, k);
                if (ni < 0 || nj < 0 || nk < 0) continue;
                if (f[ni + 1][nj + 1][nk + 1] == remain - 1) {
                    res.append(ch);
                    i = ni + 1;
                    j = nj + 1;
                    k = nk + 1;
                    remain--;
                    break;
                }
            }
        }
        System.out.println(res.toString());
    }
}
