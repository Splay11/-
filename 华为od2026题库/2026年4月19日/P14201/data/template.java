import java.io.*;
import java.nio.charset.StandardCharsets;

public class Main {
    private static String parseInput() throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));
        StringBuilder sb = new StringBuilder();
        String line;
        boolean first = true;
        while ((line = br.readLine()) != null) {
            if (!first) {
                sb.append('\n');
            }
            sb.append(line);
            first = false;
        }
        String data = sb.toString().trim();
        if (data.isEmpty()) {
            return "";
        }
        if (data.length() >= 2 && data.charAt(0) == '"' && data.charAt(data.length() - 1) == '"') {
            return data.substring(1, data.length() - 1);
        }
        return data;
    }

    public static void main(String[] args) throws Exception {
        String instructions = parseInput();
        Solution solution = new Solution();
        int result = solution.processInstructions(instructions);
        System.out.print(result);
    }
}
