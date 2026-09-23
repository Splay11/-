import java.io.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();

        // 解析三个逗号分隔的值：capacity,efficiency,scene
        String[] parts = line.split(",");
        double capacity = Double.parseDouble(parts[0].trim());
        double efficiency = Double.parseDouble(parts[1].trim());
        int scene = Integer.parseInt(parts[2].trim());

        Solution solution = new Solution();
        System.out.println(solution.calculateRange(capacity, efficiency, scene));
    }
}
