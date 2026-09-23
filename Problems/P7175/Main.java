import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Main {
    // 按运算符把左右两个子表达式的值合在一起
    static int combine(int a, char op, int b) {
        if (op == '+') {
            return a + b;
        }
        if (op == '-') {
            return a - b;
        }
        return a * b;
    }

    // 连续数字合成一个整数；12 必须当成十二，不能拆成 1 和 2
    static void parse(String expression, List<Integer> nums, List<Character> ops) {
        int i = 0;
        int n = expression.length();
        while (i < n) {
            char ch = expression.charAt(i);
            if (ch == '+' || ch == '-' || ch == '*') {
                ops.add(ch);
                i++;
            } else {
                int val = 0;
                while (i < n) {
                    char d = expression.charAt(i);
                    if (d < '0' || d > '9') {
                        break;
                    }
                    val = val * 10 + (d - '0');
                    i++;
                }
                nums.add(val);
            }
        }
    }

    // 计算 nums[left..right] 所有加括号方式；枚举最后一次运算的位置
    static List<Integer> dfs(int left, int right, List<Integer> nums, List<Character> ops,
                             List<Integer>[][] memo) {
        if (memo[left][right] != null) {
            return memo[left][right];
        }
        List<Integer> res = new ArrayList<Integer>();
        if (left == right) {
            res.add(nums.get(left));
            memo[left][right] = res;
            return res;
        }
        for (int k = left; k < right; k++) {
            List<Integer> leftVals = dfs(left, k, nums, ops, memo);
            List<Integer> rightVals = dfs(k + 1, right, nums, ops, memo);
            char op = ops.get(k);
            for (int i = 0; i < leftVals.size(); i++) {
                for (int j = 0; j < rightVals.size(); j++) {
                    res.add(combine(leftVals.get(i), op, rightVals.get(j)));
                }
            }
        }
        memo[left][right] = res;
        return res;
    }

    static List<Integer> solve(String expression) {
        List<Integer> nums = new ArrayList<Integer>();
        List<Character> ops = new ArrayList<Character>();
        parse(expression, nums, ops);
        int m = nums.size();
        @SuppressWarnings("unchecked")
        List<Integer>[][] memo = new ArrayList[m][m];
        List<Integer> vals = dfs(0, m - 1, nums, ops, memo);
        Collections.sort(vals);
        return vals;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String expression = br.readLine().trim();
        List<Integer> vals = solve(expression);
        StringBuilder sb = new StringBuilder();
        sb.append(vals.size()).append('\n');
        for (int i = 0; i < vals.size(); i++) {
            if (i > 0) {
                sb.append(' ');
            }
            sb.append(vals.get(i));
        }
        sb.append('\n');
        System.out.print(sb.toString());
    }
}
