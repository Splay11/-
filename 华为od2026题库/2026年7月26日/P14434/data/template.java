import java.io.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;

        int n = line.length();
        int i = 0;
        // 跳过首部空白，定位到每个引号内部的字符串
        while (i < n && line.charAt(i) != '"') i++;
        i++; // 跳过起始引号
        StringBuilder num = new StringBuilder();
        while (i < n && line.charAt(i) != '"')
            num.append(line.charAt(i++));
        i++; // 跳过结束引号

        while (i < n && line.charAt(i) != '"') i++;
        i++;
        StringBuilder sourceDigits = new StringBuilder();
        while (i < n && line.charAt(i) != '"')
            sourceDigits.append(line.charAt(i++));
        i++;

        while (i < n && line.charAt(i) != '"') i++;
        i++;
        StringBuilder targetDigits = new StringBuilder();
        while (i < n && line.charAt(i) != '"')
            targetDigits.append(line.charAt(i++));

        Solution solution = new Solution();
        System.out.println('"' + solution.convertNumber(
            num.toString(), sourceDigits.toString(), targetDigits.toString()
        ) + '"');
    }
}
