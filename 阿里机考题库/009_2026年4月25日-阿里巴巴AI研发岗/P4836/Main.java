import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Main {
    public static String solveOne(int length, String tag) {
        // rightCnt 统计当前位右侧尚未处理的原标签字符数量
        int[] rightCnt = new int[26];
        for (int i = 0; i < length; i++) {
            rightCnt[tag.charAt(i) - 'a']++;
        }

        // leftCnt 统计左侧已校正完成的最终字符数量
        int[] leftCnt = new int[26];

        StringBuilder ans = new StringBuilder();

        for (int i = 0; i < length; i++) {
            char ch = tag.charAt(i);
            int idx = ch - 'a';

            // 当前字符不再属于右侧，先从右侧计数中删去
            rightCnt[idx]--;

            // leftCnt：左侧最终字符中等于当前 glyph 的个数
            int leftCntVal = leftCnt[idx];

            // rightCnt：右侧原串中等于当前 glyph 的个数
            int rightCntVal = rightCnt[idx];

            int newIdx;

            // 两侧计数相等则轮询到下一个小写字母
            if (leftCntVal == rightCntVal) {
                newIdx = (idx + 1) % 26;
            } else {
                newIdx = idx;
            }

            ans.append((char) ('a' + newIdx));
            leftCnt[newIdx]++;
        }

        return ans.toString();
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        int tc = Integer.parseInt(br.readLine().trim());

        for (int i = 0; i < tc; i++) {
            int length = Integer.parseInt(br.readLine().trim());
            String tag = br.readLine().trim();

            System.out.println(solveOne(length, tag));
        }
    }
}
