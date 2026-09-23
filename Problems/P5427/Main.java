import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;
import java.util.Scanner;

public class Main {
    // 分解 x 的全部不同质因数。1 没有质因数。
    static List<Integer> primeFactors(int x) {
        List<Integer> factors = new ArrayList<>();
        if (x <= 1) {
            return factors;
        }
        if (x % 2 == 0) {
            factors.add(2);
            while (x % 2 == 0) {
                x /= 2;
            }
        }
        for (int d = 3; (long) d * d <= x; d += 2) {
            if (x % d == 0) {
                factors.add(d);
                while (x % d == 0) {
                    x /= d;
                }
            }
        }
        // 剩下大于 1 的就是最后一个质数
        if (x > 1) {
            factors.add(x);
        }
        return factors;
    }

    // 从下标 0 出发 BFS，边为 ±质因数且不越界
    static boolean canReach(int[] seq) {
        int m = seq.length;
        // 只有一个位置时，起点就是终点
        if (m == 1) {
            return true;
        }
        boolean[] vis = new boolean[m];
        Deque<Integer> q = new ArrayDeque<>();
        vis[0] = true;
        q.addLast(0);
        while (!q.isEmpty()) {
            int p = q.removeFirst();
            for (int d : primeFactors(seq[p])) {
                int[] cand = {p + d, p - d};
                for (int nxt : cand) {
                    if (nxt < 0 || nxt >= m || vis[nxt]) {
                        continue;
                    }
                    if (nxt == m - 1) {
                        return true;
                    }
                    vis[nxt] = true;
                    q.addLast(nxt);
                }
            }
        }
        return false;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        // 一行空格分隔的整个序列
        String[] parts = sc.nextLine().trim().split("\\s+");
        int[] seq = new int[parts.length];
        for (int i = 0; i < parts.length; i++) {
            seq[i] = Integer.parseInt(parts[i]);
        }
        sc.close();
        System.out.println(canReach(seq) ? "true" : "false");
    }
}
