import java.util.*;

public class Main {
    
    // 定义活动类
    static class Activity {
        int start;
        int end;

        public Activity(int start, int end) {
            this.start = start;
            this.end = end;
        }
    }

    // 计算最多可以选择的活动数
    public static int maxActivities(int n, List<Activity> activities) {
        // 1. 按照活动的结束时间排序
        activities.sort(Comparator.comparingInt(a -> a.end));

        // 2. 初始化选中的活动数量和上一个活动的结束时间
        int count = 0;
        int lastEndTime = -1;

        // 3. 遍历所有活动，选择不与前一个活动重叠的活动
        for (Activity activity : activities) {
            if (activity.start > lastEndTime) {  // 当前活动开始时间大于上一个活动结束时间
                count++;
                lastEndTime = activity.end;  // 更新上一个活动的结束时间为当前活动的结束时间
            }
        }

        return count;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int n = sc.nextInt();  // 输入活动数量
        List<Activity> activities = new ArrayList<>();

        for (int i = 0; i < n; i++) {
            int start = sc.nextInt();
            int end = sc.nextInt();
            activities.add(new Activity(start, end));  // 输入每个活动的开始时间和结束时间
        }

        // 输出最多可以选择的活动数
        System.out.println(maxActivities(n, activities));

        sc.close();
    }
}
