import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;

public class Main {
    // 按出现次数从高到低排，次数相同按字符 ASCII；同一字符必须连在一起
    static String solve(String s) {
        int[] cnt = new int[256];
        for (int i = 0; i < s.length(); i++) {
            cnt[s.charAt(i)]++;
        }
        ArrayList<int[]> items = new ArrayList<int[]>();
        for (int c = 0; c < 256; c++) {
            if (cnt[c] > 0) {
                items.add(new int[] {cnt[c], c});
            }
        }
        Collections.sort(items, new Comparator<int[]>() {
            public int compare(int[] a, int[] b) {
                if (a[0] != b[0]) {
                    return b[0] - a[0];
                }
                return a[1] - b[1];
            }
        });
        StringBuilder sb = new StringBuilder(s.length());
        for (int i = 0; i < items.size(); i++) {
            int times = items.get(i)[0];
            char ch = (char) items.get(i)[1];
            for (int k = 0; k < times; k++) {
                sb.append(ch);
            }
        }
        return sb.toString();
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        System.out.println(solve(s));
    }
}
