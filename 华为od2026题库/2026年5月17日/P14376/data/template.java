import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    public static void main(String[] args) throws Exception {
        // 读取一行 IPv4 地址，readLine 会自动去掉行末换行符
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String ip = br.readLine();
        if (ip == null) {
            ip = "";
        }

        // 调用用户实现的函数并输出结果
        Solution solution = new Solution();
        System.out.print(solution.classifyIPv4(ip));
    }
}
