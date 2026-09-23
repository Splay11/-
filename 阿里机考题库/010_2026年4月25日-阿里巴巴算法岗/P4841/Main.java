import java.util.*;

public class Main {

    static long solveOne(int cnt, long seed, int[] modSet) {
        int mn = modSet[0], maxMod = modSet[0];
        for (int v : modSet) {
            mn = Math.min(mn, v);
            maxMod = Math.max(maxMod, v);
        }

        // 种子已小于最小模数，后续折减均不改变当前值
        if (seed < mn) return seed;

        boolean[] exist = new boolean[maxMod + 1];
        ArrayList<Integer> mods = new ArrayList<>();
        for (int v : modSet) {
            if (!exist[v]) {
                exist[v] = true;
                mods.add(v);
            }
        }

        boolean[] vis = new boolean[maxMod + 1];
        Queue<Integer> q = new LinkedList<>();

        // 第一次有效折减：seed mod order_i
        for (int a : mods) {
            if (a <= seed) {
                int r = (int) (seed % a);
                if (!vis[r]) {
                    vis[r] = true;
                    q.offer(r);
                }
            }
        }

        // BFS 枚举所有可达的 cur
        while (!q.isEmpty()) {
            int cur = q.poll();
            for (int a : mods) {
                if (a <= cur) {
                    int nxt = cur % a;
                    if (!vis[nxt]) {
                        vis[nxt] = true;
                        q.offer(nxt);
                    }
                }
            }
        }

        // 最终余值必须严格小于 mn
        int ans = 0;
        for (int i = 0; i < mn; i++) {
            if (vis[i]) ans = i;
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int T = sc.nextInt();
        StringBuilder sb = new StringBuilder();

        for (int tc = 0; tc < T; tc++) {
            int cnt = sc.nextInt();
            long seed = sc.nextLong();
            int[] modSet = new int[cnt];
            for (int i = 0; i < cnt; i++) modSet[i] = sc.nextInt();
            sb.append(solveOne(cnt, seed, modSet)).append('\n');
        }

        System.out.print(sb.toString());
        sc.close();
    }
}
