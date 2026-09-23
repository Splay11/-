import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int R = Integer.parseInt(st.nextToken());
        int C = Integer.parseInt(st.nextToken());
        List<String[]> plans = new ArrayList<>();
        for (int i = 0; i < R; i++) {
            st = new StringTokenizer(br.readLine());
            plans.add(new String[]{st.nextToken(), st.nextToken(), st.nextToken()});
        }
        Set<String> ready = new HashSet<>();
        for (int i = 0; i < C; i++) {
            st = new StringTokenizer(br.readLine());
            String rid = st.nextToken();
            String ver = st.nextToken();
            String plat = st.nextToken();
            String status = st.nextToken();
            if (status.equals("READY")) ready.add(rid + "\0" + ver + "\0" + plat);
        }
        List<String> missing = new ArrayList<>();
        for (String[] p : plans) {
            String rid = p[0], ver = p[2];
            boolean ok = ready.contains(rid + "\0" + ver + "\0android")
                    && ready.contains(rid + "\0" + ver + "\0ios")
                    && ready.contains(rid + "\0" + ver + "\0pc");
            if (!ok) missing.add(rid);
        }
        if (missing.isEmpty()) {
            System.out.println("none");
        } else {
            for (String x : missing) System.out.println(x);
        }
    }
}
