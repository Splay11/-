// Java 评测模板
import java.io.IOException;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        Scanner sc = new Scanner(System.in);
        String str = sc.nextLine();
        str = str.replace("[", "").replace("]", "").replace(" ", "");
        //System.out.println(str);
        String[] strs = str.split(",");
        
        List<InvokeInfo> invokes = new ArrayList<>();
        for (int i = 0; i < strs.length; i += 2) {
            int time = Integer.parseInt(strs[i]);
            int interfaceId = Integer.parseInt(strs[i+1]);
            invokes.add(new InvokeInfo(interfaceId, time));      
        }

        int timeSegment = sc.nextInt();
        int minLimits = sc.nextInt();
        
        System.out.println(new Solution().getInterfaces(invokes, timeSegment, minLimits));

    }
}