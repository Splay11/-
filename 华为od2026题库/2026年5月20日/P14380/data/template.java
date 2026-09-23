import java.io.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;

        int n = Integer.parseInt(line.trim());

        Solution solution = new Solution();
        System.out.println(solution.equalDistanceBinary(n));
    }
}
