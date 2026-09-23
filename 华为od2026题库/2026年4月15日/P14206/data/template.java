// HydroOJ 函数题模式 Java 模板文件
// 说明：
// 1. 本文件负责输入解析、调用用户实现的函数、输出结果
// 2. 用户需要在 user.java 中实现 Solution 类的 mergeLogs 方法
// 3. 输入格式示例：
//    ["/api/user","/api/user","/api/order"],[100,200,150]

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

public class Main {

    // 解析字符串数组，例如：["/a","/b","/c"]
    private static String[] parseStringArray(String s) {
        List<String> list = new ArrayList<>();
        int n = s.length();
        int i = 0;

        // 跳过起始空白和左括号
        while (i < n && Character.isWhitespace(s.charAt(i))) {
            i++;
        }
        if (i < n && s.charAt(i) == '[') {
            i++;
        }

        while (i < n) {
            // 跳过空白和逗号
            while (i < n && (Character.isWhitespace(s.charAt(i)) || s.charAt(i) == ',')) {
                i++;
            }

            // 遇到右括号则结束
            if (i < n && s.charAt(i) == ']') {
                break;
            }

            // 解析一个带双引号的字符串
            if (i < n && s.charAt(i) == '"') {
                i++;
                StringBuilder sb = new StringBuilder();

                while (i < n) {
                    char c = s.charAt(i);

                    // 处理转义字符
                    if (c == '\\' && i + 1 < n) {
                        char next = s.charAt(i + 1);
                        // 保留常见转义后的实际字符
                        if (next == '"' || next == '\\' || next == '/') {
                            sb.append(next);
                            i += 2;
                        } else if (next == 'n') {
                            sb.append('\n');
                            i += 2;
                        } else if (next == 't') {
                            sb.append('\t');
                            i += 2;
                        } else if (next == 'r') {
                            sb.append('\r');
                            i += 2;
                        } else {
                            // 其他情况直接按原字符追加
                            sb.append(next);
                            i += 2;
                        }
                    } else if (c == '"') {
                        i++;
                        break;
                    } else {
                        sb.append(c);
                        i++;
                    }
                }

                list.add(sb.toString());
            } else {
                // 输入格式合法时不会进入这里，做容错处理
                i++;
            }
        }

        return list.toArray(new String[0]);
    }

    // 解析整数数组，例如：[100,200,150]
    private static int[] parseIntArray(String s) {
        String cleaned = s.trim();
        if (cleaned.length() == 0 || cleaned.equals("[]")) {
            return new int[0];
        }

        // 去掉首尾方括号
        if (cleaned.charAt(0) == '[') {
            cleaned = cleaned.substring(1);
        }
        if (cleaned.length() > 0 && cleaned.charAt(cleaned.length() - 1) == ']') {
            cleaned = cleaned.substring(0, cleaned.length() - 1);
        }

        cleaned = cleaned.trim();
        if (cleaned.length() == 0) {
            return new int[0];
        }

        String[] parts = cleaned.split(",");
        int[] nums = new int[parts.length];
        for (int i = 0; i < parts.length; i++) {
            nums[i] = Integer.parseInt(parts[i].trim());
        }
        return nums;
    }

    // 将总输入拆分成两个数组片段
    private static String[] splitTwoParts(String input) {
        int n = input.length();
        int level = 0;
        boolean inString = false;
        int splitPos = -1;

        for (int i = 0; i < n; i++) {
            char c = input.charAt(i);

            // 处理字符串中的转义符，避免误判
            if (c == '\\' && inString && i + 1 < n) {
                i++;
                continue;
            }

            if (c == '"') {
                inString = !inString;
            } else if (!inString) {
                if (c == '[') {
                    level++;
                } else if (c == ']') {
                    level--;
                } else if (c == ',' && level == 0) {
                    splitPos = i;
                    break;
                }
            }
        }

        if (splitPos == -1) {
            // 容错：若输入不完整，则按两个空数组处理
            return new String[] {"[]", "[]"};
        }

        String part1 = input.substring(0, splitPos).trim();
        String part2 = input.substring(splitPos + 1).trim();
        return new String[] {part1, part2};
    }

    // 将二维整型数组格式化输出为类似 [[0,2,150],[2,1,150]]
    private static String format2DIntArray(int[][] arr) {
        StringBuilder sb = new StringBuilder();
        sb.append("[");

        for (int i = 0; i < arr.length; i++) {
            if (i > 0) {
                sb.append(",");
            }
            sb.append("[");
            for (int j = 0; j < arr[i].length; j++) {
                if (j > 0) {
                    sb.append(",");
                }
                sb.append(arr[i][j]);
            }
            sb.append("]");
        }

        sb.append("]");
        return sb.toString();
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder inputBuilder = new StringBuilder();
        String line;

        while ((line = br.readLine()) != null) {
            inputBuilder.append(line.trim());
        }

        String input = inputBuilder.toString().trim();

        String[] parts = splitTwoParts(input);
        String[] paths = parseStringArray(parts[0]);
        int[] responseTimes = parseIntArray(parts[1]);

        // 调用用户实现
        int[][] ans = new Solution().mergeLogs(paths, responseTimes);

        // 输出结果
        System.out.print(format2DIntArray(ans));
    }
}
