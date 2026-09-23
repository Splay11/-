import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Main {
    static boolean canClear(String s) {
        // 每次核销都同时去掉一个 0 和一个 1
        // 只要两种字符都还在，串里一定存在相邻的 01 或 10
        // 所以能删空当且仅当 0 和 1 的个数相等
        int c0 = 0, c1 = 0;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '0') {
                c0++;
            } else {
                c1++;
            }
        }
        return c0 == c1;
    }

    static int countClearable(List<String> strs) {
        int ans = 0;
        for (int i = 0; i < strs.size(); i++) {
            if (canClear(strs.get(i))) {
                ans++;
            }
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int m = sc.nextInt();
        List<String> strs = new ArrayList<String>();
        for (int i = 0; i < m; i++) {
            strs.add(sc.next());
        }
        System.out.println(countClearable(strs));
        sc.close();
    }
}
