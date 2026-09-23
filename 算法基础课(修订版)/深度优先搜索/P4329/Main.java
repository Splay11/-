import java.util.*;

public class Main {
    static final int MOD = 1000000007;
    static List<Integer>[] adj; // 邻接表
    static int[] ops; // 运算类型数组

    // 计算节点值
    static long cc(long a, long b, int t) {
        return (t == 0) ? (a + b) % MOD : (a * b) % MOD;
    }

    // 递归计算节点 u 的权值
    static long cal(int u) {
        if (adj[u].size() == 2) {
            return cc(cal(adj[u].get(0)), cal(adj[u].get(1)), ops[u]);
        }
        return 1; // 叶子节点权值固定为 1
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int num = sc.nextInt();

        adj = new ArrayList[num];
        ops = new int[num];

        for (int i = 0; i < num; i++) {
            adj[i] = new ArrayList<>();
        }

        // 读取父子关系
        for (int i = 1; i < num; i++) {
            int parent = sc.nextInt();
            adj[parent - 1].add(i);
        }

        // 读取运算类型
        for (int i = 0; i < num; i++) {
            ops[i] = sc.nextInt();
        }

        // 计算并输出根节点权值
        System.out.println(cal(0));
        sc.close();
    }
}
