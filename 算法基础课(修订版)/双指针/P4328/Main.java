import java.util.*;
import java.io.*;

public class Main {
    // 统计二进制数组中至多有 k 个 1 的子数组数量
    public static long countAtMostK(int[] b, int k){
        int left = 0;
        long result = 0;
        int count = 0;
        for(int right = 0; right < b.length; right++){
            if(b[right] == 1){
                count++;
            }
            while(count > k){
                if(b[left] == 1){
                    count--;
                }
                left++;
            }
            result += (right - left + 1);
        }
        return result;
    }
    
    public static void main(String[] args) throws IOException{
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        // 读取第一行，整数序列 a
        String line = br.readLine();
        String[] tokens = line.trim().split("\\s+");
        int n = tokens.length;
        int[] a = new int[n];
        for(int i = 0; i < n; i++) a[i] = Integer.parseInt(tokens[i]);
        // 读取第二行，x 和 k
        line = br.readLine();
        tokens = line.trim().split("\\s+");
        int x = Integer.parseInt(tokens[0]);
        int k = Integer.parseInt(tokens[1]);
        // 将 a 映射为二进制数组 b，1 表示能被 x 整除，0 否则
        int[] b = new int[n];
        for(int i = 0; i < n; i++){
            if(a[i] % x == 0){
                b[i] = 1;
            }
        }
        // 计算答案
        long total = countAtMostK(b, k);
        if(k > 0){
            total -= countAtMostK(b, k-1);
        }
        System.out.println(total);
    }
}
