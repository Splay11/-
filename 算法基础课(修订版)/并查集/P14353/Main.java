import java.util.Scanner;

public class Main {
    static int[] parent;

    static void init(int n) {
        parent = new int[n + 1];
        for (int i = 1; i <= n; i++) {
            parent[i] = i;
        }
    }

    static int find(int x) {
        if (parent[x] != x)
            parent[x] = find(parent[x]); // 路径压缩
        return parent[x];
    }

    static void union(int x, int y) {
        int xRoot = find(x);
        int yRoot = find(y);
        if (xRoot != yRoot)
            parent[xRoot] = yRoot;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt(), m = sc.nextInt();
        init(n);
        for (int i = 0; i < m; i++) {
            int z = sc.nextInt(), x = sc.nextInt(), y = sc.nextInt();
            if (z == 1) {
                union(x, y);
            } else {
                System.out.println(find(x) == find(y) ? "Y" : "N");
            }
        }
        sc.close();
    }
}
