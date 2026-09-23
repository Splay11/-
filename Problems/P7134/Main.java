import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.StringTokenizer;

public class Main {
    static final int MAX_ID = 50000;

    // 从 kill 出发走完整棵子树，把所有会被杀掉的进程收集起来再排序
    // 用栈做 DFS，n 可以到 5e4，链状树递归会爆
    static List<Integer> solve(int[] pids, int[] ppids, int kill) {
        @SuppressWarnings("unchecked")
        List<Integer>[] children = new ArrayList[MAX_ID + 1];
        for (int i = 0; i <= MAX_ID; i++) {
            children[i] = new ArrayList<>();
        }
        for (int i = 0; i < pids.length; i++) {
            // 父进程为 0 的是根，没有人再指向它的父亲
            if (ppids[i] != 0) {
                children[ppids[i]].add(pids[i]);
            }
        }
        List<Integer> killed = new ArrayList<>();
        List<Integer> stack = new ArrayList<>();
        stack.add(kill);
        while (!stack.isEmpty()) {
            int u = stack.remove(stack.size() - 1);
            killed.add(u);
            // 杀掉 u 时，它的所有孩子也会被杀掉
            for (int v : children[u]) {
                stack.add(v);
            }
        }
        // 题面要求按进程 ID 从小到大输出
        Collections.sort(killed);
        return killed;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int kill = Integer.parseInt(st.nextToken());
        st = new StringTokenizer(br.readLine());
        int[] pids = new int[n];
        for (int i = 0; i < n; i++) {
            pids[i] = Integer.parseInt(st.nextToken());
        }
        st = new StringTokenizer(br.readLine());
        int[] ppids = new int[n];
        for (int i = 0; i < n; i++) {
            ppids[i] = Integer.parseInt(st.nextToken());
        }
        List<Integer> ans = solve(pids, ppids, kill);
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < ans.size(); i++) {
            if (i > 0) {
                sb.append(' ');
            }
            sb.append(ans.get(i));
        }
        System.out.println(sb);
    }
}
