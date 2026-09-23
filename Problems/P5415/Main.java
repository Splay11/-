import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Deque;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

public class Main {
    static final String START = "Core-SW-01";

    static List<String> findPath(List<String[]> hops) {
        Map<String, List<String>> g = new HashMap<String, List<String>>();
        for (int i = 0; i < hops.size(); i++) {
            String u = hops.get(i)[0];
            String v = hops.get(i)[1];
            if (!g.containsKey(u)) {
                g.put(u, new ArrayList<String>());
            }
            g.get(u).add(v);
        }
        for (List<String> vs : g.values()) {
            vs.sort(Comparator.reverseOrder());
        }
        List<String> route = new ArrayList<String>();
        Deque<String> st = new ArrayDeque<String>();
        st.push(START);
        while (!st.isEmpty()) {
            String u = st.peek();
            List<String> vs = g.get(u);
            if (vs != null && !vs.isEmpty()) {
                // 出边已按终点名字从大到小排，弹出末尾就是当前更小的终点
                // 有未用跳转就继续往前走，把终点压栈
                // 没有出边才记下当前点，相当于后序，死胡同会先出现在答案尾部
                // 这样不会像纯贪心那样走进死胡同就再也回不来
                String v = vs.remove(vs.size() - 1);
                st.push(v);
            } else {
                route.add(u);
                st.pop();
            }
        }
        Collections.reverse(route);
        return route;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        List<String[]> hops = new ArrayList<String[]>();
        while (sc.hasNext()) {
            String u = sc.next();
            if (!sc.hasNext()) {
                break;
            }
            String v = sc.next();
            hops.add(new String[] {u, v});
        }
        List<String> ans = findPath(hops);
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < ans.size(); i++) {
            if (i > 0) {
                sb.append(' ');
            }
            sb.append(ans.get(i));
        }
        System.out.println(sb.toString());
        sc.close();
    }
}
