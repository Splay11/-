import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

public class Main {
    private static List<Long> parseNumbers(String text) {
        // 将除数字和负号以外的字符全部替换成空格，再统一按数字流解析
        StringBuilder sb = new StringBuilder(text.length());
        for (int i = 0; i < text.length(); i++) {
            char c = text.charAt(i);
            if ((c >= '0' && c <= '9') || c == '-') {
                sb.append(c);
            } else {
                sb.append(' ');
            }
        }

        List<Long> nums = new ArrayList<>();
        StringTokenizer st = new StringTokenizer(sb.toString());
        while (st.hasMoreTokens()) {
            nums.add(Long.parseLong(st.nextToken()));
        }
        return nums;
    }

    private static String formatResult(List<List<Long>> result) {
        // 将二维数组按题目要求格式化为紧凑输出
        StringBuilder sb = new StringBuilder();
        sb.append('[');
        for (int i = 0; i < result.size(); i++) {
            if (i > 0) {
                sb.append(',');
            }
            sb.append('[');
            List<Long> row = result.get(i);
            for (int j = 0; j < row.size(); j++) {
                if (j > 0) {
                    sb.append(',');
                }
                sb.append(row.get(j));
            }
            sb.append(']');
        }
        sb.append(']');
        return sb.toString();
    }

    public static void main(String[] args) throws Exception {
        // 读取完整输入
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder inputBuilder = new StringBuilder();
        String line;
        while ((line = br.readLine()) != null) {
            if (inputBuilder.length() > 0) {
                inputBuilder.append('\n');
            }
            inputBuilder.append(line);
        }

        String input = inputBuilder.toString().trim();
        if (input.isEmpty()) {
            System.out.print("[]");
            return;
        }

        // 解析所有数字
        List<Long> nums = parseNumbers(input);
        if (nums.size() < 2) {
            System.out.print("[]");
            return;
        }

        int n = nums.get(0).intValue();
        int k = nums.get(1).intValue();

        // 将后续数字按 [id, priority] 两两组装成 packets
        List<List<Long>> packets = new ArrayList<>();
        for (int i = 2; i + 1 < nums.size() && packets.size() < n; i += 2) {
            List<Long> packet = new ArrayList<>(2);
            packet.add(nums.get(i));
            packet.add(nums.get(i + 1));
            packets.add(packet);
        }

        // 调用用户实现的核心函数
        Solution solution = new Solution();
        List<List<Long>> result = solution.processPackets(n, k, packets);

        // 输出结果
        System.out.print(formatResult(result));
    }
}
