import java.io.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();

        // 解析输入："lights",t
        int start = line.indexOf('"');
        int end = line.indexOf('"', start + 1);
        String lights = line.substring(start + 1, end);

        // 逗号后的整数
        int comma = line.indexOf(',', end);
        int t = Integer.parseInt(line.substring(comma + 1).trim());

        Solution solution = new Solution();
        String result = solution.lightStripTransform(lights, t);
        System.out.println("\"" + result + "\"");
    }
}
