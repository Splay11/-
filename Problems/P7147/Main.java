import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

public class Main {
    // 用栈模拟碰撞：只有栈顶向右、当前向左才会撞
    static List<Integer> solve(int[] asteroids) {
        List<Integer> stack = new ArrayList<>();
        for (int x : asteroids) {
            boolean alive = true;
            // 只有「右行遇上左行」才会碰撞
            while (alive && !stack.isEmpty() && stack.get(stack.size() - 1) > 0 && x < 0) {
                int top = stack.get(stack.size() - 1);
                if (Math.abs(top) < Math.abs(x)) {
                    // 栈顶更小，炸掉栈顶，当前小行星继续往左撞
                    stack.remove(stack.size() - 1);
                    continue;
                }
                if (Math.abs(top) == Math.abs(x)) {
                    // 一样大，两颗一起炸
                    stack.remove(stack.size() - 1);
                }
                // 栈顶更大或已经同归于尽，当前这颗不再存活
                alive = false;
            }
            if (alive) {
                stack.add(x);
            }
        }
        return stack;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        StringTokenizer st = new StringTokenizer(br.readLine());
        int[] a = new int[n];
        for (int i = 0; i < n; i++) {
            a[i] = Integer.parseInt(st.nextToken());
        }
        List<Integer> rest = solve(a);
        System.out.println(rest.size());
        // 没有剩余时只输出 0，不要再打空的第二行
        if (!rest.isEmpty()) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < rest.size(); i++) {
                if (i > 0) {
                    sb.append(' ');
                }
                sb.append(rest.get(i));
            }
            System.out.println(sb.toString());
        }
    }
}
