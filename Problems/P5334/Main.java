import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.StringTokenizer;

public class Main {
    // 按层搭建三角栈道，求从 start 出发的无向欧拉回路
    static ArrayList<Integer> solve(int h, int start) {
        int n = h * (h + 1) / 2;
        ArrayList<Integer>[] g = new ArrayList[n + 1];
        for (int i = 1; i <= n; i++) {
            g[i] = new ArrayList<Integer>();
        }
        ArrayList<Integer> eu = new ArrayList<Integer>();
        ArrayList<Integer> ev = new ArrayList<Integer>();

        // 加入一条无向栈道，两端都记下边号
        for (int r = 2; r <= h; r++) {
            // base / prev 分别是本层、上一层「编号减一」的偏移
            int base = r * (r - 1) / 2;
            int prev = (r - 1) * (r - 2) / 2;
            for (int c = 1; c < r; c++) {
                int u = base + c;
                int v = base + c + 1;
                int w = prev + c;
                add(g, eu, ev, u, v);
                add(g, eu, ev, u, w);
                add(g, eu, ev, v, w);
            }
        }

        int m = eu.size();
        boolean[] used = new boolean[m];
        int[] ptr = new int[n + 1];
        ArrayList<Integer> stack = new ArrayList<Integer>();
        ArrayList<Integer> circ = new ArrayList<Integer>();
        stack.add(start);
        // Hierholzer：沿未用边走，走不通时把点弹入回路（得到逆序）
        while (!stack.isEmpty()) {
            int u = stack.get(stack.size() - 1);
            while (ptr[u] < g[u].size() && used[g[u].get(ptr[u])]) {
                ptr[u]++;
            }
            if (ptr[u] == g[u].size()) {
                circ.add(u);
                stack.remove(stack.size() - 1);
            } else {
                int eid = g[u].get(ptr[u]);
                ptr[u]++;
                used[eid] = true;
                int a = eu.get(eid);
                int b = ev.get(eid);
                stack.add(a == u ? b : a);
            }
        }
        Collections.reverse(circ);
        return circ;
    }

    static void add(ArrayList<Integer>[] g, ArrayList<Integer> eu, ArrayList<Integer> ev, int a, int b) {
        int eid = eu.size();
        eu.add(a);
        ev.add(b);
        g[a].add(eid);
        g[b].add(eid);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
        int k = Integer.parseInt(br.readLine().trim());
        for (int t = 0; t < k; t++) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            int h = Integer.parseInt(st.nextToken());
            int s = Integer.parseInt(st.nextToken());
            ArrayList<Integer> path = solve(h, s);
            for (int i = 0; i < path.size(); i++) {
                if (i > 0) {
                    bw.write(' ');
                }
                bw.write(Integer.toString(path.get(i)));
            }
            bw.write('\n');
        }
        bw.flush();
    }
}
