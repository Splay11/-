import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    // 用栈消除相邻相同字母
    static String solve(String s) {
        int n = s.length();
        char[] stack = new char[n];
        int top = 0;
        for (int i = 0; i < n; i++) {
            char c = s.charAt(i);
            if (top > 0 && stack[top - 1] == c) {
                // 相邻相同，成对删除
                top--;
            } else {
                stack[top++] = c;
            }
        }
        return new String(stack, 0, top);
    }

    public static void main(String[] args) throws IOException {
        // 一整行小写字母
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        System.out.println(solve(s));
    }
}
