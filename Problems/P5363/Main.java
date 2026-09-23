import java.util.ArrayDeque;
import java.util.Queue;
import java.util.Scanner;

public class Main {
    static int maxDepth(String t) {
        // 空树
        if (t.equals("{}")) {
            return 0;
        }
        // 去掉花括号后按逗号切开层序
        String[] vals = t.substring(1, t.length() - 1).split(",", -1);
        Queue<Integer> q = new ArrayDeque<Integer>();
        q.add(0);
        int idx = 1;
        int depth = 0;
        while (!q.isEmpty()) {
            // 当前层每个真实探头把深度加一
            depth++;
            int sz = q.size();
            for (int k = 0; k < sz; k++) {
                q.poll();
                // 至多读两个孩子；末尾省略则停止
                if (idx < vals.length) {
                    if (!vals[idx].equals("#")) {
                        q.add(idx);
                    }
                    idx++;
                }
                if (idx < vals.length) {
                    if (!vals[idx].equals("#")) {
                        q.add(idx);
                    }
                    idx++;
                }
            }
        }
        return depth;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String t = "";
        if (sc.hasNextLine()) {
            t = sc.nextLine().trim();
        }
        System.out.println(maxDepth(t));
        sc.close();
    }
}
