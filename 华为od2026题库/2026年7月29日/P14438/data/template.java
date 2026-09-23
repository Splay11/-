import java.util.*;
import java.io.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();

        // 解析 R
        int c1 = line.indexOf(',');
        int R = Integer.parseInt(line.substring(0, c1).trim());

        // 解析 G
        String rest1 = line.substring(c1 + 1);
        int c2 = rest1.indexOf(',');
        int G = Integer.parseInt(rest1.substring(0, c2).trim());

        // 剩余部分: [E,S,W,N],[0,1,3,6]
        String rest2 = rest1.substring(c2 + 1);
        int split = rest2.indexOf("],[");
        String dirsStr = rest2.substring(0, split + 1);   // [E,S,W,N]
        String timesStr = rest2.substring(split + 3);       // 0,1,3,6]

        // 解析方向字符列表
        List<Character> directions = new ArrayList<>();
        StringBuilder cur = new StringBuilder();
        for (int i = 1; i < dirsStr.length(); i++) {
            char ch = dirsStr.charAt(i);
            if (ch == ',' || ch == ']') {
                if (cur.length() > 0) {
                    directions.add(cur.charAt(0));
                    cur.setLength(0);
                }
                if (ch == ']') break;
            } else if (ch != ' ') {
                cur.append(ch);
            }
        }
        if (cur.length() > 0) directions.add(cur.charAt(0));

        char[] dirsArr = new char[directions.size()];
        for (int i = 0; i < directions.size(); i++) {
            dirsArr[i] = directions.get(i);
        }

        // 解析到达时间列表
        List<Integer> arrivalTimes = new ArrayList<>();
        cur.setLength(0);
        for (int i = 0; i < timesStr.length(); i++) {
            char ch = timesStr.charAt(i);
            if (ch == ',' || ch == ']') {
                if (cur.length() > 0) {
                    arrivalTimes.add(Integer.parseInt(cur.toString().trim()));
                    cur.setLength(0);
                }
                if (ch == ']') break;
            } else {
                cur.append(ch);
            }
        }
        if (cur.length() > 0) arrivalTimes.add(Integer.parseInt(cur.toString().trim()));

        int[] timesArr = new int[arrivalTimes.size()];
        for (int i = 0; i < arrivalTimes.size(); i++) {
            timesArr[i] = arrivalTimes.get(i);
        }

        Solution solution = new Solution();
        int[] result = solution.intersectionWaitingTime(R, G, dirsArr, timesArr);
        System.out.println("[" + result[0] + "," + result[1] + "]");
    }
}
