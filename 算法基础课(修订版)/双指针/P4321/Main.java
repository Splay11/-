import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        // 读第一行 n, m
        String line = br.readLine();
        while (line != null && line.trim().isEmpty()) line = br.readLine();
        StringTokenizer st = new StringTokenizer(line);
        int n = Integer.parseInt(st.nextToken());
        int m = Integer.parseInt(st.nextToken());

        // 读字符串 s
        String s = br.readLine().trim();

        // 构建矛盾矩阵
        boolean[][] conflict = new boolean[26][26];
        for (int i = 0; i < m; i++) {
            String lm = br.readLine();
            while (lm != null && lm.trim().isEmpty()) lm = br.readLine();
            StringTokenizer st2 = new StringTokenizer(lm);
            String a = st2.nextToken();
            String b = st2.nextToken();
            int ia = a.charAt(0) - 'A';
            int ib = b.charAt(0) - 'A';
            if (ia != ib) {
                conflict[ia][ib] = true;
                conflict[ib][ia] = true;
            }
        }

        int[] last = new int[26];
        Arrays.fill(last, -1);

        int l = 0;
        long ans = 0L; // 注意可能很大，用 long
        for (int r = 0; r < n; r++) {
            int c = s.charAt(r) - 'A';
            // 推进 l，去除与 c 冲突的字母
            for (int x = 0; x < 26; x++) {
                if (conflict[c][x] && last[x] >= l) {
                    l = last[x] + 1;
                }
            }
            // 以 r 结尾的和谐子串个数
            ans += (r - l + 1);
            // 更新最近出现位置
            last[c] = r;
        }

        System.out.println(ans);
    }
}
