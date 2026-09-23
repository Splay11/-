import java.util.ArrayDeque;
import java.util.Scanner;

public class Main {
    static boolean canQueue(String u, String v) {
        return u.equals(v);
    }

    static boolean canStack(String u, String v) {
        ArrayDeque<Character> st = new ArrayDeque<Character>();
        int i = 0;
        int n = u.length();
        // 按出站序列贪心：栈顶不匹配就继续入站
        for (int k = 0; k < v.length(); ++k) {
            char c = v.charAt(k);
            while (i < n && (st.isEmpty() || st.peekLast() != c)) {
                st.addLast(u.charAt(i));
                ++i;
            }
            if (st.isEmpty() || st.peekLast() != c) {
                return false;
            }
            st.removeLast();
        }
        return true;
    }

    static String solve(String u, String v) {
        boolean q = canQueue(u, v);
        boolean s = canStack(u, v);
        if (q && s) return "both";
        if (q) return "queue";
        if (s) return "stack";
        return "neither";
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String u = sc.next();
        String v = sc.next();
        System.out.println(solve(u, v));
        sc.close();
    }
}
