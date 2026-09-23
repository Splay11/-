import java.util.ArrayList;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Scanner;

public class Main {
    static int[] parseVer(String s) {
        // 把 a.b.c 拆成三个整数，按三段比较
        String[] p = s.split("\\.");
        return new int[] {Integer.parseInt(p[0]), Integer.parseInt(p[1]), Integer.parseInt(p[2])};
    }

    static int cmpVer(int[] x, int[] y) {
        for (int i = 0; i < 3; i++) {
            if (x[i] != y[i]) {
                return x[i] < y[i] ? -1 : 1;
            }
        }
        return 0;
    }

    static class Dep {
        int pid;
        String op;
        int[] bound;
    }

    static Dep parseDep(String token) {
        // 先匹配两位运算符，避免把 >= 拆成 >
        String[] ops = {">=", "<=", ">", "<"};
        Dep d = new Dep();
        for (int i = 0; i < ops.length; i++) {
            int pos = token.indexOf(ops[i]);
            if (pos != -1) {
                d.pid = Integer.parseInt(token.substring(0, pos));
                d.op = ops[i];
                d.bound = parseVer(token.substring(pos + ops[i].length()));
                return d;
            }
        }
        d.pid = Integer.parseInt(token);
        d.op = null;
        return d;
    }

    static boolean versionOk(int[] actual, Dep d) {
        if (d.op == null) {
            return true;
        }
        int c = cmpVer(actual, d.bound);
        if (d.op.equals(">=")) {
            return c >= 0;
        }
        if (d.op.equals("<=")) {
            return c <= 0;
        }
        if (d.op.equals(">")) {
            return c > 0;
        }
        return c < 0;
    }

    static String installOrder(int m, int[] pids, int[][] vers, List<List<String>> deps) {
        int[][] verOf = new int[m][3];
        List<List<String>> depOf = new ArrayList<List<String>>();
        for (int i = 0; i < m; i++) {
            depOf.add(new ArrayList<String>());
        }
        for (int i = 0; i < m; i++) {
            verOf[pids[i]] = vers[i];
            depOf.set(pids[i], deps.get(i));
        }

        // 先检查全部版本约束，有冲突直接 -1
        for (int pid = 0; pid < m; pid++) {
            for (int j = 0; j < depOf.get(pid).size(); j++) {
                Dep d = parseDep(depOf.get(pid).get(j));
                if (!versionOk(verOf[d.pid], d)) {
                    return "-1";
                }
            }
        }

        // 边从被依赖者指向依赖者：先安装被依赖者
        List<List<Integer>> g = new ArrayList<List<Integer>>();
        int[] indeg = new int[m];
        for (int i = 0; i < m; i++) {
            g.add(new ArrayList<Integer>());
        }
        for (int pid = 0; pid < m; pid++) {
            for (int j = 0; j < depOf.get(pid).size(); j++) {
                Dep d = parseDep(depOf.get(pid).get(j));
                g.get(d.pid).add(pid);
                indeg[pid]++;
            }
        }

        // 小根堆保证每次取出当前可安装编号最小的包
        PriorityQueue<Integer> heap = new PriorityQueue<Integer>();
        for (int i = 0; i < m; i++) {
            if (indeg[i] == 0) {
                heap.add(i);
            }
        }
        List<Integer> order = new ArrayList<Integer>();
        while (!heap.isEmpty()) {
            int u = heap.poll();
            order.add(u);
            for (int k = 0; k < g.get(u).size(); k++) {
                int v = g.get(u).get(k);
                indeg[v]--;
                if (indeg[v] == 0) {
                    heap.add(v);
                }
            }
        }
        // 没能装完说明有环（含自己依赖自己）
        if (order.size() != m) {
            return "-2";
        }
        StringBuilder ans = new StringBuilder();
        for (int i = 0; i < m; i++) {
            if (i > 0) {
                ans.append(" ");
            }
            ans.append(order.get(i));
        }
        return ans.toString();
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int m = sc.nextInt();
        sc.nextLine();
        int[] pids = new int[m];
        int[][] vers = new int[m][3];
        List<List<String>> deps = new ArrayList<List<String>>();
        for (int i = 0; i < m; i++) {
            String line = sc.nextLine().trim();
            String[] parts = line.split("\\s+");
            pids[i] = Integer.parseInt(parts[0]);
            vers[i] = parseVer(parts[1]);
            List<String> ds = new ArrayList<String>();
            for (int j = 2; j < parts.length; j++) {
                ds.add(parts[j]);
            }
            deps.add(ds);
        }
        System.out.println(installOrder(m, pids, vers, deps));
        sc.close();
    }
}
