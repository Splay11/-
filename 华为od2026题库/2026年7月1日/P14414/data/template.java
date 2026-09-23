import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();

        // 解析：N,K,M,[a1,a2,...,aN]
        int pos1 = line.indexOf(',');
        int N = Integer.parseInt(line.substring(0, pos1));

        int pos2 = line.indexOf(',', pos1 + 1);
        int K = Integer.parseInt(line.substring(pos1 + 1, pos2));

        int pos3 = line.indexOf(',', pos2 + 1);
        int M = Integer.parseInt(line.substring(pos2 + 1, pos3));

        // 解析数组
        String arrStr = line.substring(pos3 + 1).trim();
        if (arrStr.startsWith("[")) arrStr = arrStr.substring(1);
        if (arrStr.endsWith("]")) arrStr = arrStr.substring(0, arrStr.length() - 1);

        List<Integer> A = new ArrayList<>();
        if (!arrStr.isEmpty()) {
            String[] parts = arrStr.split(",");
            for (String p : parts) {
                A.add(Integer.parseInt(p.trim()));
            }
        }

        Solution solution = new Solution();
        System.out.println(solution.maxSpiritPower(N, K, M, A));
    }
}
