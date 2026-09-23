import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Main {
    static boolean isValid(String t) {
        // 栈里只放还没配上的开封口；遇闭封口必须立刻配栈顶
        List<Character> st = new ArrayList<Character>();
        for (int i = 0; i < t.length(); i++) {
            char ch = t.charAt(i);
            if (ch == '(' || ch == '[' || ch == '{') {
                // 开封口：入栈等待
                st.add(ch);
            } else {
                // 闭封口：栈空或种类对不上则非法
                if (st.isEmpty()) {
                    return false;
                }
                char top = st.get(st.size() - 1);
                if ((ch == ')' && top != '(') || (ch == ']' && top != '[') || (ch == '}' && top != '{')) {
                    return false;
                }
                st.remove(st.size() - 1);
            }
        }
        // 还有没扣上的开封口则不合格
        return st.isEmpty();
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String t = "";
        // 空文件没有下一行，按空串处理
        if (sc.hasNextLine()) {
            t = sc.nextLine();
        }
        if (isValid(t)) {
            System.out.println("true");
        } else {
            System.out.println("false");
        }
        sc.close();
    }
}
