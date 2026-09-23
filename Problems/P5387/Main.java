import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.StringTokenizer;

public class Main {
    // 按 (v+t) 的奇偶分成两类：奇类只能配偶类，偶类之间可以互配
    static ArrayList<int[]> maxPairs(int t, int[] v) {
        ArrayList<Integer> ev = new ArrayList<Integer>();
        ArrayList<Integer> od = new ArrayList<Integer>();
        for (int i = 0; i < v.length; i++) {
            if ((v[i] + t) % 2 == 0) {
                ev.add(v[i]);
            } else {
                od.add(v[i]);
            }
        }
        ArrayList<int[]> pairs = new ArrayList<int[]>();
        if (od.size() > ev.size()) {
            // 偶类不够，全部拿去配奇类
            for (int i = 0; i < ev.size(); i++) {
                pairs.add(new int[] {ev.get(i), od.get(i)});
            }
        } else {
            // 先把奇类配完，剩下的偶类两两互配
            for (int i = 0; i < od.size(); i++) {
                pairs.add(new int[] {od.get(i), ev.get(i)});
            }
            for (int i = od.size(); i + 1 < ev.size(); i += 2) {
                pairs.add(new int[] {ev.get(i), ev.get(i + 1)});
            }
        }
        return pairs;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        PrintWriter out = new PrintWriter(System.out);
        StringTokenizer st = new StringTokenizer(br.readLine());
        int m = Integer.parseInt(st.nextToken());
        int t = Integer.parseInt(st.nextToken());
        st = new StringTokenizer(br.readLine());
        int[] v = new int[m];
        for (int i = 0; i < m; i++) {
            v[i] = Integer.parseInt(st.nextToken());
        }
        ArrayList<int[]> pairs = maxPairs(t, v);
        out.println(pairs.size());
        for (int i = 0; i < pairs.size(); i++) {
            out.println(pairs.get(i)[0] + " " + pairs.get(i)[1]);
        }
        out.flush();
    }
}
