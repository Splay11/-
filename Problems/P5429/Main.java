import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Main {
    // 按编号升序回溯，枚举长度为 t 的无冲突组合
    static void dfs(int start, int m, int t, int g, int lo, int hi, int[] w,
                    List<Integer> chosen, int total, int[] count, List<List<Integer>> top) {
        // 已经取满 t 个：只检查负荷和
        if (chosen.size() == t) {
            if (lo <= total && total <= hi) {
                count[0]++;
                if (top.size() < 3) {
                    top.add(new ArrayList<>(chosen));
                }
            }
            return;
        }
        int remain = t - chosen.size();
        // 从 start 起枚举下一个编号；编号必须递增，保证字典序
        for (int i = start; i <= m; i++) {
            // 剩下位置不够凑满 t 个，后面更大的 i 更不够
            if (m - i + 1 < remain) {
                break;
            }
            chosen.add(i);
            // 下一个合法起点至少是 i+g+1，这样相邻差一定大于 g
            dfs(i + g + 1, m, t, g, lo, hi, w, chosen, total + w[i - 1], count, top);
            chosen.remove(chosen.size() - 1);
        }
    }

    static int collectSchemes(int m, int t, int g, int lo, int hi, int[] w, List<List<Integer>> top) {
        int[] count = new int[1];
        dfs(1, m, t, g, lo, hi, w, new ArrayList<>(), 0, count, top);
        return count[0];
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int m = sc.nextInt();
        int t = sc.nextInt();
        int g = sc.nextInt();
        int lo = sc.nextInt();
        int hi = sc.nextInt();
        int[] w = new int[m];
        for (int i = 0; i < m; i++) {
            w[i] = sc.nextInt();
        }
        sc.close();
        List<List<Integer>> top = new ArrayList<>();
        int count = collectSchemes(m, t, g, lo, hi, w, top);
        System.out.println(count);
        for (List<Integer> scheme : top) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < scheme.size(); i++) {
                if (i > 0) {
                    sb.append(' ');
                }
                sb.append(scheme.get(i));
            }
            System.out.println(sb);
        }
    }
}
