import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Main {
    // 用栈按段处理 Unix 路径
    static String solve(String path) {
        List<String> stack = new ArrayList<>();
        int n = path.length();
        int i = 0;
        while (i < n) {
            // 跳过斜杠，连续多个 / 只当一个
            while (i < n && path.charAt(i) == '/') {
                i++;
            }
            if (i >= n) {
                break;
            }
            int j = i;
            while (j < n && path.charAt(j) != '/') {
                j++;
            }
            String part = path.substring(i, j);
            i = j;
            if (part.equals(".")) {
                // 当前目录，忽略
                continue;
            }
            if (part.equals("..")) {
                // 已经在根目录时不能再往上走
                if (!stack.isEmpty()) {
                    stack.remove(stack.size() - 1);
                }
            } else {
                // ... 等其他名字都是普通目录
                stack.add(part);
            }
        }
        if (stack.isEmpty()) {
            return "/";
        }
        StringBuilder ans = new StringBuilder();
        for (String name : stack) {
            ans.append('/').append(name);
        }
        return ans.toString();
    }

    public static void main(String[] args) throws IOException {
        // 读入一整行绝对路径
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String path = br.readLine();
        // 输出规范路径
        System.out.println(solve(path));
    }
}
