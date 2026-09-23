import java.util.*;

public class Main {
    static int[][] child;
    static int nodeCnt;

    // 将一个读数插入二进制字典树
    static void insert(int x) {
        int node = 0;
        for (int b = 30; b >= 0; b--) {
            int bit = (x >> b) & 1;
            if (child[node][bit] == 0) {
                child[node][bit] = nodeCnt++;
            }
            node = child[node][bit];
        }
    }

    // 查询与 x 异或能得到的最大值
    static int queryMaxXor(int x) {
        int node = 0;
        int res = 0;

        for (int b = 30; b >= 0; b--) {
            int bit = (x >> b) & 1;
            int want = bit ^ 1;

            // 优先走相反位，使当前位异或结果为 1
            if (child[node][want] != 0) {
                res |= 1 << b;
                node = child[node][want];
            } else {
                node = child[node][bit];
            }
        }

        return res;
    }

    // 计算每个位置是否可行
    static String solveArray(int[] v) {
        int n = v.length;
        int M = 0;  // 序列最大值

        for (int x : v) {
            M = Math.max(M, x);
        }

        // 最多 n * 31 个节点，0 号节点作为根
        child = new int[n * 31 + 5][2];
        nodeCnt = 1;

        char[] ans = new char[n];
        Arrays.fill(ans, '0');

        // 从右往左维护后缀字典树
        for (int i = n - 1; i >= 0; i--) {
            if (i < n - 1) {
                int best = queryMaxXor(v[i]);
                if (best >= M) {
                    ans[i] = '1';
                }
            }

            // 当前读数插入，供左侧位置查询
            insert(v[i]);
        }

        return new String(ans);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int n = sc.nextInt();
        int[] v = new int[n];

        for (int i = 0; i < n; i++) {
            v[i] = sc.nextInt();
        }

        System.out.println(solveArray(v));
    }
}
