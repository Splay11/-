import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.ArrayDeque;
import java.util.Deque;

public class Main {
    // 用栈解码嵌套的 k[串]
    static String solve(String s) {
        Deque<String> strs = new ArrayDeque<>();
        Deque<Integer> nums = new ArrayDeque<>();
        StringBuilder cur = new StringBuilder();
        int num = 0;
        int n = s.length();
        for (int i = 0; i < n; i++) {
            char c = s.charAt(i);
            if (c >= '0' && c <= '9') {
                // k 可能有多位，例如 300
                num = num * 10 + (c - '0');
            } else if (c == '[') {
                // 进入新一层括号，外层结果先存起来
                strs.addLast(cur.toString());
                nums.addLast(num);
                cur.setLength(0);
                num = 0;
            } else if (c == ']') {
                int k = nums.removeLast();
                String prev = strs.removeLast();
                // 内层解码结果重复 k 次，再接到外层后面
                String inner = cur.toString();
                StringBuilder next = new StringBuilder(prev);
                for (int t = 0; t < k; t++) {
                    next.append(inner);
                }
                cur = next;
            } else {
                cur.append(c);
            }
        }
        return cur.toString();
    }

    public static void main(String[] args) throws IOException {
        // 不含空格，整行就是编码串
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        System.out.println(solve(s));
    }
}
