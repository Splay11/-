import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();

        // 提取全部整数：前 3 个为 n, m, w，其余每 3 个为一条路线
        int[] a = extractInts(line);
        int n = a[0], m = a[1], w = a[2];
        int[][] roads = new int[(a.length - 3) / 3][3];
        for (int i = 3, k = 0; i + 2 < a.length; i += 3, k++) {
            roads[k][0] = a[i];
            roads[k][1] = a[i + 1];
            roads[k][2] = a[i + 2];
        }

        Solution sol = new Solution();
        int ans = sol.minCost(n, m, w, roads);
        System.out.println(ans);
    }

    // 从字符串中提取所有整数（忽略非数字字符）
    static int[] extractInts(String s) {
        ArrayList<Integer> list = new ArrayList<>();
        int cur = 0, have = 0;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c >= '0' && c <= '9') {
                cur = cur * 10 + (c - '0');
                have = 1;
            } else if (have == 1) {
                list.add(cur);
                cur = 0;
                have = 0;
            }
        }
        if (have == 1) list.add(cur);
        int[] res = new int[list.size()];
        for (int i = 0; i < res.length; i++) res[i] = list.get(i);
        return res;
    }
}
