import java.io.*;
import java.util.*;

public class Main {
    static void dfs(int[] a, int start, int target, List<Integer> path, List<List<Integer>> ans) {
        if (target == 0) {
            ans.add(new ArrayList<>(path));
            return;
        }
        for (int i = start; i < a.length; i++) {
            if (i > start && a[i] == a[i - 1]) continue; // 同层去重
            if (a[i] > target) break;                    // 剪枝
            path.add(a[i]);
            dfs(a, i + 1, target - a[i], path, ans);     // 每个数只能用一次
            path.remove(path.size() - 1);
        }
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner(System.in);
        Integer nObj = fs.nextInt();
        if (nObj == null) return;
        int n = nObj;
        int[] a = new int[n];
        for (int i = 0; i < n; i++) a[i] = fs.nextInt();
        int target = fs.nextInt();

        Arrays.sort(a);
        List<List<Integer>> ans = new ArrayList<>();
        dfs(a, 0, target, new ArrayList<>(), ans);

        // 按字典序排序
        ans.sort((u, v) -> {
            int m = Math.min(u.size(), v.size());
            for (int i = 0; i < m; i++) {
                int cmp = Integer.compare(u.get(i), v.get(i));
                if (cmp != 0) return cmp;
            }
            return Integer.compare(u.size(), v.size());
        });

        if (ans.isEmpty()) {
            System.out.println();
            return;
        }
        StringBuilder sb = new StringBuilder();
        for (List<Integer> comb : ans) {
            for (int i = 0; i < comb.size(); i++) {
                if (i > 0) sb.append(' ');
                sb.append(comb.get(i));
            }
            sb.append('\n');
        }
        System.out.print(sb.toString());
    }

    // 轻量读入
    static class FastScanner {
        private final InputStream in;
        private final byte[] buffer = new byte[1 << 16];
        private int ptr = 0, len = 0;
        FastScanner(InputStream is) { in = is; }
        private int read() throws IOException {
            if (ptr >= len) {
                len = in.read(buffer);
                ptr = 0;
                if (len <= 0) return -1;
            }
            return buffer[ptr++];
        }
        Integer nextInt() throws IOException {
            String s = next();
            return s == null ? null : Integer.parseInt(s);
        }
        String next() throws IOException {
            StringBuilder sb = new StringBuilder();
            int c;
            while ((c = read()) != -1 && Character.isWhitespace(c));
            if (c == -1) return null;
            do { sb.append((char)c); } while ((c = read()) != -1 && !Character.isWhitespace(c));
            return sb.toString();
        }
    }
}
