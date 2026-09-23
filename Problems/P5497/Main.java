import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    static int findRoot(int[] parent, long[] delta, int x) {
        // 找到根，并把途中点的差额改成相对根：delta[x] = 付款[x] - 付款[根]
        if (parent[x] != x) {
            int root = findRoot(parent, delta, parent[x]);
            delta[x] += delta[parent[x]];
            parent[x] = root;
            return root;
        }
        return x;
    }

    static int[] process(int n, int k, int[] floorOf, int[] qa, int[] qb, long[] qx) {
        int[] parent = new int[n + 1];
        // delta[x]：x 比当前父亲多付的钱；路径压缩后变成比根多付的钱
        long[] delta = new long[n + 1];
        int[] sz = new int[n + 1];
        for (int i = 1; i <= n; i++) {
            parent[i] = i;
            sz[i] = 1;
        }
        int invalid = 0;
        int q = qa.length;
        for (int i = 0; i < q; i++) {
            int a = qa[i];
            int b = qb[i];
            long x = qx[i];
            // 自己跟自己比，差额只能是 0
            if (a == b) {
                if (x != 0) {
                    invalid++;
                }
                continue;
            }
            int ra = findRoot(parent, delta, a);
            int rb = findRoot(parent, delta, b);
            if (ra == rb) {
                // 两人已在同一圈：推出的差额必须正好是 x
                if (delta[a] - delta[b] != x) {
                    invalid++;
                }
                continue;
            }
            // 不同圈：楼层不同或合并后人数超 K，本条作废
            if (floorOf[a] != floorOf[b] || sz[ra] + sz[rb] > k) {
                invalid++;
                continue;
            }
            // 记下 pay[a] - pay[b] = x，小圈挂到大圈下面
            if (sz[ra] < sz[rb]) {
                parent[ra] = rb;
                delta[ra] = x - delta[a] + delta[b];
                sz[rb] += sz[ra];
            } else {
                parent[rb] = ra;
                delta[rb] = delta[a] - delta[b] - x;
                sz[ra] += sz[rb];
            }
        }
        int circles = 0;
        for (int i = 1; i <= n; i++) {
            if (parent[i] == i) {
                circles++;
            }
        }
        return new int[] {invalid, circles};
    }

    public static void main(String[] args) throws IOException {
        // n、q 到 1e5，用 BufferedReader
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int q = Integer.parseInt(st.nextToken());
        int k = Integer.parseInt(st.nextToken());
        st = new StringTokenizer(br.readLine());
        int[] floorOf = new int[n + 1];
        for (int i = 1; i <= n; i++) {
            floorOf[i] = Integer.parseInt(st.nextToken());
        }
        int[] qa = new int[q];
        int[] qb = new int[q];
        long[] qx = new long[q];
        for (int i = 0; i < q; i++) {
            st = new StringTokenizer(br.readLine());
            qa[i] = Integer.parseInt(st.nextToken());
            qb[i] = Integer.parseInt(st.nextToken());
            qx[i] = Long.parseLong(st.nextToken());
        }
        int[] ans = process(n, k, floorOf, qa, qb, qx);
        System.out.println(ans[0]);
        System.out.println(ans[1]);
    }
}
