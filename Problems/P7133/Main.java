import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

public class Main {
    static final int MAX_ID = 2000;

    // 从 start 出发走完整棵下属树，把沿途每人的重要度加起来
    // 用栈做 DFS，避免链状组织把递归撑爆
    static int solve(int[] importance, List<Integer>[] children, int start) {
        int total = 0;
        List<Integer> stack = new ArrayList<>();
        stack.add(start);
        while (!stack.isEmpty()) {
            int u = stack.remove(stack.size() - 1);
            total += importance[u];
            // 把直属下属压栈，之后会继续走到间接下属
            for (int v : children[u]) {
                stack.add(v);
            }
        }
        return total;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int qid = Integer.parseInt(st.nextToken());
        // 下标直接当员工 ID 用，题目保证 1..2000
        int[] importance = new int[MAX_ID + 1];
        @SuppressWarnings("unchecked")
        List<Integer>[] children = new ArrayList[MAX_ID + 1];
        for (int i = 0; i <= MAX_ID; i++) {
            children[i] = new ArrayList<>();
        }
        for (int i = 0; i < n; i++) {
            st = new StringTokenizer(br.readLine());
            int eid = Integer.parseInt(st.nextToken());
            int imp = Integer.parseInt(st.nextToken());
            int m = Integer.parseInt(st.nextToken());
            importance[eid] = imp;
            // m=0 时这一行没有后续下属 id
            for (int j = 0; j < m; j++) {
                children[eid].add(Integer.parseInt(st.nextToken()));
            }
        }
        System.out.println(solve(importance, children, qid));
    }
}
