import java.io.*;
import java.util.*;

public class Main {
    static List<int[]> schemes = new ArrayList<>();
    static int[] path;
    static int n;

    // 回溯枚举：当前人 idx，剩余苹果 remain
    static void dfs(int remain, int idx) {
        if (idx == n - 1) {
            // 最后一人拿完剩余
            path[idx] = remain;
            schemes.add(path.clone());
            return;
        }
        // 从小到大枚举，保证字典序
        for (int x = 0; x <= remain; x++) {
            path[idx] = x;
            dfs(remain - x, idx + 1);
        }
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] sp = br.readLine().trim().split("\\s+");
        int m = Integer.parseInt(sp[0]);
        n = Integer.parseInt(sp[1]);
        path = new int[n];
        dfs(m, 0);
        StringBuilder sb = new StringBuilder();
        for (int[] s : schemes) {
            for (int i = 0; i < n; i++) {
                if (i > 0) sb.append(' ');
                sb.append(s[i]);
            }
            sb.append('\n');
        }
        sb.append(schemes.size());
        System.out.println(sb.toString());
    }
}
