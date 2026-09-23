import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null || line.trim().isEmpty()) return;

        // 预处理字符串：将 [ ] , " 替换为空格，方便提取有效信息
        String processed = line.replace("[", " ").replace("]", " ").replace(",", " ").replace("\"", " ");
        Scanner sc = new Scanner(processed);
        
        if (!sc.hasNextInt()) return;
        int month = sc.nextInt();
        
        List<String> allTokens = new ArrayList<>();
        while (sc.hasNext()) {
            allTokens.add(sc.next());
        }
        
        // 由于 employees 和 birthdays 长度一致，平分剩余的 token
        int n = allTokens.size() / 2;
        List<String> employees = new ArrayList<>();
        List<String> birthdays = new ArrayList<>();
        
        for (int i = 0; i < n; i++) employees.add(allTokens.get(i));
        for (int i = 0; i < n; i++) birthdays.add(allTokens.get(n + i));

        Solution solution = new Solution();
        System.out.print(solution.countBirthdayGifts(month, employees, birthdays));
    }
}
