import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        String[] sp = br.readLine().trim().split("\\s+");
        int[] p = new int[n];
        for (int i = 0; i < n; i++) p[i] = Integer.parseInt(sp[i]);

        // 最小交换次数 = n - 环个数
        boolean[] vis = new boolean[n];
        int cycles = 0;
        for (int i = 0; i < n; i++) {
            if (vis[i]) continue;
            cycles++;
            int j = i;
            // 沿置换走完一个环
            while (!vis[j]) {
                vis[j] = true;
                j = p[j] - 1;
            }
        }
        System.out.println(n - cycles);
    }
}
