import java.io.*;
import java.util.*;
import java.nio.charset.StandardCharsets;

public class Main {
    private static int 查找匹配右括号(String s, int 左括号位置) {
        int 深度 = 0;
        for (int i = 左括号位置; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '[') {
                深度++;
            } else if (c == ']') {
                深度--;
                if (深度 == 0) {
                    return i;
                }
            }
        }
        return s.length() - 1;
    }

    private static int[] 解析一维数组(String 片段) {
        String 清理后 = 片段.replace('[', ' ').replace(']', ' ').replace(',', ' ');
        Scanner scanner = new Scanner(清理后);
        ArrayList<Integer> nums = new ArrayList<>();

        while (scanner.hasNextInt()) {
            nums.add(scanner.nextInt());
        }
        scanner.close();

        int[] arr = new int[nums.size()];
        for (int i = 0; i < nums.size(); i++) {
            arr[i] = nums.get(i);
        }
        return arr;
    }

    private static int[][] 解析二维数组(String 片段) {
        int[] flat = 解析一维数组(片段);
        int 行数 = flat.length / 3;
        int[][] pipes = new int[行数][3];

        for (int i = 0; i < 行数; i++) {
            pipes[i][0] = flat[i * 3];
            pipes[i][1] = flat[i * 3 + 1];
            pipes[i][2] = flat[i * 3 + 2];
        }
        return pipes;
    }

    private static String 输出数组(int[] arr) {
        StringBuilder sb = new StringBuilder();
        sb.append('[');
        for (int i = 0; i < arr.length; i++) {
            if (i > 0) {
                sb.append(',');
            }
            sb.append(arr[i]);
        }
        sb.append(']');
        return sb.toString();
    }

    public static void main(String[] args) throws Exception {
        String input = new String(System.in.readAllBytes(), StandardCharsets.UTF_8).trim();
        if (input.length() == 0) {
            return;
        }

        int 第一个逗号 = input.indexOf(',');
        int n = Integer.parseInt(input.substring(0, 第一个逗号).trim());

        int sources左括号 = input.indexOf('[', 第一个逗号 + 1);
        int sources右括号 = 查找匹配右括号(input, sources左括号);
        String sources片段 = input.substring(sources左括号, sources右括号 + 1);

        int pipes左括号 = input.indexOf('[', sources右括号 + 1);
        String pipes片段;
        if (pipes左括号 == -1) {
            pipes片段 = "[]";
        } else {
            int pipes右括号 = 查找匹配右括号(input, pipes左括号);
            pipes片段 = input.substring(pipes左括号, pipes右括号 + 1);
        }

        int[] sources = 解析一维数组(sources片段);
        int[][] pipes = 解析二维数组(pipes片段);

        Solution solution = new Solution();
        int[] ans = solution.findIsolatedStations(n, sources, pipes);
        System.out.println(输出数组(ans));
    }
}
