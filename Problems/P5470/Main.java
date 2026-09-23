import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.StringTokenizer;

public class Main {
    // 最少波次 = DAG 上最长链包含的模型个数
    static int minWaves(int p, int[][] rel) {
        ArrayList<Integer>[] graph = new ArrayList[p + 1];
        for (int i = 1; i <= p; i++) {
            graph[i] = new ArrayList<Integer>();
        }
        int[] indeg = new int[p + 1];
        for (int k = 0; k < rel.length; k++) {
            int u = rel[k][0];
            int v = rel[k][1];
            graph[u].add(v);
            indeg[v]++;
        }

        // dp[x]：以 x 结尾的最长链长度；孤立点为 1
        int[] dp = new int[p + 1];
        for (int i = 1; i <= p; i++) {
            dp[i] = 1;
        }
        ArrayDeque<Integer> q = new ArrayDeque<Integer>();
        for (int i = 1; i <= p; i++) {
            if (indeg[i] == 0) {
                q.add(i);
            }
        }

        while (!q.isEmpty()) {
            int u = q.poll();
            for (int v : graph[u]) {
                // 先走完 u 再走 v，链长至少是 dp[u] + 1
                if (dp[u] + 1 > dp[v]) {
                    dp[v] = dp[u] + 1;
                }
                indeg[v]--;
                if (indeg[v] == 0) {
                    q.add(v);
                }
            }
        }

        int ans = 1;
        for (int i = 1; i <= p; i++) {
            if (dp[i] > ans) {
                ans = dp[i];
            }
        }
        return ans;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int p = Integer.parseInt(st.nextToken());
        int e = Integer.parseInt(st.nextToken());
        int[][] rel = new int[e][2];
        for (int k = 0; k < e; k++) {
            st = new StringTokenizer(br.readLine());
            rel[k][0] = Integer.parseInt(st.nextToken());
            rel[k][1] = Integer.parseInt(st.nextToken());
        }
        System.out.println(minWaves(p, rel));
    }
}
