import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null || line.trim().isEmpty()) {
            return;
        }

        String[] parts = line.trim().split(",");
        int M = Integer.parseInt(parts[0].trim());
        int N = Integer.parseInt(parts[1].trim());

        Solution s = new Solution();
        System.out.print(s.getNthValue(M, N));
    }
}
