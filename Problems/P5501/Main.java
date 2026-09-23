import java.util.ArrayList;
import java.util.Scanner;

public class Main {
    static String process(String s) {
        // 先去掉所有 b
        StringBuilder buf = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch != 'b') {
                buf.append(ch);
            }
        }
        // 再用栈消除连续的 ac（可反复相邻形成）
        ArrayList<Character> st = new ArrayList<Character>();
        for (int i = 0; i < buf.length(); i++) {
            char ch = buf.charAt(i);
            if (!st.isEmpty() && st.get(st.size() - 1) == 'a' && ch == 'c') {
                st.remove(st.size() - 1);
            } else {
                st.add(ch);
            }
        }
        StringBuilder ans = new StringBuilder();
        for (char c : st) {
            ans.append(c);
        }
        return ans.toString();
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine().trim();
        System.out.println(process(s));
        sc.close();
    }
}
