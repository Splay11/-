import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();
        if (line.startsWith("\"") && line.endsWith("\"")) {
            line = line.substring(1, line.length() - 1);
        }

        Solution solution = new Solution();
        int[] ans = solution.timeClassification(line);

        // 输出格式严格没有空格
        System.out.print("[");
        for (int i = 0; i < ans.length; i++) {
            if (i > 0) System.out.print(",");
            System.out.print(ans[i]);
        }
        System.out.println("]");
    }
}
