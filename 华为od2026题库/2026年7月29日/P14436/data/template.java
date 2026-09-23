import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();

        int comma = line.indexOf(',');
        int n = Integer.parseInt(line.substring(0, comma));

        String arrStr = line.substring(comma + 1).trim();
        List<Integer> energies = new ArrayList<>();
        if (arrStr.length() > 2) {
            String inner = arrStr.substring(1, arrStr.length() - 1);
            String[] parts = inner.split(",");
            for (String p : parts) {
                energies.add(Integer.parseInt(p.trim()));
            }
        }

        Solution sol = new Solution();
        List<Integer> result = sol.energyCollision(energies);

        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < result.size(); i++) {
            if (i > 0) sb.append(',');
            sb.append(result.get(i));
        }
        sb.append(']');
        System.out.println(sb.toString());
    }
}
