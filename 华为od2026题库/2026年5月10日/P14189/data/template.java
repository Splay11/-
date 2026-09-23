import java.io.*;
import java.util.*;

// 模板只负责读取输入、调用用户实现并输出结果
class Main {
    // 将逗号、括号等分隔符统一替换为空格，再用输入流思想提取整数
    private static List<Long> parseInput(String text) {
        StringBuilder normalized = new StringBuilder();

        for (int i = 0; i < text.length(); i++) {
            char ch = text.charAt(i);
            if ((ch >= '0' && ch <= '9') || ch == '-') {
                normalized.append(ch);
            } else {
                normalized.append(' ');
            }
        }

        List<Long> nums = new ArrayList<>();
        StringTokenizer st = new StringTokenizer(normalized.toString());
        while (st.hasMoreTokens()) {
            nums.add(Long.parseLong(st.nextToken()));
        }
        return nums;
    }

    public static void main(String[] args) throws Exception {
        StringBuilder input = new StringBuilder();
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        String line;
        while ((line = br.readLine()) != null) {
            input.append(line).append(' ');
        }

        List<Long> nums = parseInput(input.toString());

        long capacity = nums.get(0);
        long align = nums.get(1);
        long readIndex = nums.get(2);
        long writeIndex = nums.get(3);
        long pktSize = nums.get(4);

        Solution solution = new Solution();
        long ans = solution.calcWriteIndex(
            capacity,
            align,
            readIndex,
            writeIndex,
            pktSize
        );

        System.out.println(ans);
    }
}
