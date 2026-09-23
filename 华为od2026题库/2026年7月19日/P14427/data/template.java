import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();

        // 去掉字符串两端的引号
        String record;
        if (line.length() >= 2 && line.charAt(0) == '"' && line.charAt(line.length() - 1) == '"') {
            record = line.substring(1, line.length() - 1);
        } else {
            record = line;
        }

        Solution solution = new Solution();
        List<Character> res = solution.findRepeatedServiceTypes(record);

        // 按 [r,g,m] 格式输出
        System.out.print('[');
        for (int i = 0; i < res.size(); i++) {
            if (i > 0) System.out.print(',');
            System.out.print(res.get(i));
        }
        System.out.println(']');
    }
}
