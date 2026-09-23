import java.io.*;
import java.util.*;

public class Main {
    static class DSU {
        int[] p, r;
        DSU(int n) {
            p = new int[n+1];
            r = new int[n+1];
            for (int i = 0; i <= n; i++) p[i] = i;
        }
        int find(int x) {
            if (p[x] != x) p[x] = find(p[x]);
            return p[x];
        }
        boolean unite(int a, int b) {
            a = find(a); b = find(b);
            if (a == b) return false;
            if (r[a] < r[b]) { int t = a; a = b; b = t; }
            p[b] = a;
            if (r[a] == r[b]) r[a]++;
            return true;
        }
    }

    // 快速读入
    static class FastScanner {
        BufferedInputStream in;
        byte[] buffer = new byte[1 << 16];
        int ptr = 0, len = 0;
        FastScanner(InputStream is) { in = new BufferedInputStream(is); }
        int read() throws IOException {
            if (ptr >= len) {
                len = in.read(buffer);
                ptr = 0;
                if (len <= 0) return -1;
            }
            return buffer[ptr++];
        }
        String next() throws IOException {
            StringBuilder sb = new StringBuilder();
            int c;
            while ((c = read()) <= ' ' && c != -1) {}
            if (c == -1) return null;
            do {
                sb.append((char)c);
                c = read();
            } while (c > ' ');
            return sb.toString();
        }
        Integer nextInt() throws IOException {
            String s = next();
            return s == null ? null : Integer.parseInt(s);
        }
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner(System.in);
        Integer TT = fs.nextInt();
        if (TT == null) return;
        StringBuilder ans = new StringBuilder();
        while (TT-- > 0) {
            int n = fs.nextInt(), m = fs.nextInt();

            int[] X = new int[m];
            int[] Y = new int[m];
            for (int i = 0; i < m; i++) X[i] = fs.nextInt();
            for (int i = 0; i < m; i++) Y[i] = fs.nextInt();

            boolean[][] diff = new boolean[n+1][n+1];
            for (int i = 0; i < m; i++) {
                int x = X[i], y = Y[i];
                diff[x][y] = diff[y][x] = true; // 标记不同
            }

            DSU dsu = new DSU(n);
            // 合并所有未标记为不同的对 => 认为“相同”
            for (int i = 1; i <= n; i++) {
                for (int j = i+1; j <= n; j++) {
                    if (!diff[i][j]) dsu.unite(i, j);
                }
            }

            boolean ok = true;
            // 检查每条“不同”边是否落在同一集合
            for (int i = 0; i < m && ok; i++) {
                if (dsu.find(X[i]) == dsu.find(Y[i])) ok = false;
            }

            ans.append(ok ? "Yes" : "No").append('\n');
        }
        System.out.print(ans.toString());
    }
}
