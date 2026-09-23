import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Main {
    // 单调栈贪心：每个字母只留一次，字典序尽量小
    static String solve(String s) {
        int[] last = new int[26];
        for (int k = 0; k < 26; k++) {
            last[k] = -1;
        }
        int n = s.length();
        for (int i = 0; i < n; i++) {
            // 记下每个字母最后一次出现的下标
            last[s.charAt(i) - 'a'] = i;
        }
        List<Character> stack = new ArrayList<>();
        boolean[] used = new boolean[26];
        for (int i = 0; i < n; i++) {
            char c = s.charAt(i);
            int x = c - 'a';
            if (used[x]) {
                // 已经选过，不能再出现
                continue;
            }
            while (!stack.isEmpty()) {
                char top = stack.get(stack.size() - 1);
                // 栈顶更大且后面还会出现，才能弹掉换更小前缀
                if (top > c && last[top - 'a'] > i) {
                    used[top - 'a'] = false;
                    stack.remove(stack.size() - 1);
                } else {
                    break;
                }
            }
            stack.add(c);
            used[x] = true;
        }
        StringBuilder ans = new StringBuilder();
        for (char c : stack) {
            ans.append(c);
        }
        return ans.toString();
    }

    public static void main(String[] args) throws IOException {
        // 一整行小写字母
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        System.out.println(solve(s));
    }
}
