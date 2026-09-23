import java.io.*;
import java.util.*;

public class Main {
    // 解析二维整型数组 [[p,w],[p,w],...]
    private static List<List<Integer>> parse2DArray(String s) {
        List<List<Integer>> res = new ArrayList<>();
        int start = s.indexOf('[');
        int end = s.lastIndexOf(']');
        if (start < 0 || end < 0 || end <= start) return res;
        String inner = s.substring(start + 1, end);  // 去掉外层 [ ]
        int pos = 0;
        while (pos < inner.length()) {
            int lb = inner.indexOf('[', pos);
            if (lb < 0) break;
            int rb = inner.indexOf(']', lb);
            String pairStr = inner.substring(lb + 1, rb);  // "p,w"
            int comma = pairStr.indexOf(',');
            int p = Integer.parseInt(pairStr.substring(0, comma).trim());
            int w = Integer.parseInt(pairStr.substring(comma + 1).trim());
            res.add(Arrays.asList(p, w));
            pos = rb + 1;
        }
        return res;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();

        List<List<Integer>> packets = parse2DArray(line);
        // 转为 int[][]
        int[][] arr = new int[packets.size()][2];
        for (int i = 0; i < arr.length; i++) {
            arr[i][0] = packets.get(i).get(0);
            arr[i][1] = packets.get(i).get(1);
        }

        int[] ans = new Solution().findPacket(arr);

        // 按题面样例格式输出：[id1,id2,...]（无空格）
        StringBuilder sb = new StringBuilder();
        sb.append('[');
        for (int i = 0; i < ans.length; i++) {
            sb.append(ans[i]);
            if (i + 1 < ans.length) sb.append(',');
        }
        sb.append(']');
        System.out.println(sb.toString());
    }
}
