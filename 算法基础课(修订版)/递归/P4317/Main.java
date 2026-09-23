import java.util.*;

public class Main {
    // 电话按键映射
    private static final String[] MAP = {
        "", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"
    };

    public static List<String> letterCombinations(String digits) {
        List<String> ans = new ArrayList<>();
        if (digits == null || digits.length() == 0) {
            return ans;
        }
        dfs(digits, 0, new StringBuilder(), ans);
        return ans;
    }

    // 回溯函数
    private static void dfs(String ds, int idx, StringBuilder path, List<String> ans) {
        if (idx == ds.length()) {
            ans.add(path.toString());
            return;
        }
        String letters = MAP[ds.charAt(idx) - '0'];
        for (char c : letters.toCharArray()) {
            path.append(c);             // 选择
            dfs(ds, idx + 1, path, ans); // 下层
            path.deleteCharAt(path.length() - 1); // 撤销
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine().trim();
        for (String t : letterCombinations(s)) {
            System.out.println(t);
        }
    }
}
