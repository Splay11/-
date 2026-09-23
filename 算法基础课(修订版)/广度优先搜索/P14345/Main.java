import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int a = sc.nextInt();
        int b = sc.nextInt();

        // 如果b小于1，直接输出-1
        if (b < 1) {
            System.out.println(-1);
            return;
        }

        // 定义一个数组来记录访问状态，范围到10^6
        int[] visited = new int[1000001];
        Arrays.fill(visited, -1);
        Queue<Integer> q = new LinkedList<>();

        // 从1开始
        q.add(1);
        visited[1] = 0;

        while (!q.isEmpty()) {
            int current = q.poll();

            // 如果到达目标，输出结果
            if (current == b) {
                System.out.println(visited[current]);
                return;
            }

            // 第一种魔法：乘以a
            long next1 = (long) current * a;
            if (next1 <= 1000000 && visited[(int) next1] == -1) {
                visited[(int) next1] = visited[current] + 1;
                q.add((int) next1);
            }

            // 第二种魔法：循环右移一次
            if (current >= 10 && current % 10 != 0) {
                String s = Integer.toString(current);
                String rotated = s.charAt(s.length() - 1) + s.substring(0, s.length() - 1);
                int next2 = Integer.parseInt(rotated);

                if (next2 <= 1000000 && visited[next2] == -1) {
                    visited[next2] = visited[current] + 1;
                    q.add(next2);
                }
            }
        }

        // 如果无法到达目标，输出-1
        System.out.println(-1);
    }
}
