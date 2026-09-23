import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        
        // 读取迷宫的行数和列数
        int n = sc.nextInt();
        int m = sc.nextInt();
        
        // 初始化迷宫地图
        int[][] maze = new int[n][m];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                maze[i][j] = sc.nextInt();
            }
        }
        
        int x1 = sc.nextInt(), y1 = sc.nextInt(), x2 = sc.nextInt(), y2 = sc.nextInt();
        
        // 检查起点和终点是否在迷宫范围内，并且不是墙壁
        if (x1 < 0 || x1 >= n || y1 < 0 || y1 >= m || 
            x2 < 0 || x2 >= n || y2 < 0 || y2 >= m ||
            maze[x1][y1] == 1 || maze[x2][y2] == 1) {
            System.out.println("NO");
            return;
        }
        
        // 初始化访问数组
        boolean[][] visited = new boolean[n][m];
        
        // 定义四个移动方向：上、下、左、右
        int[] dx = {-1, 1, 0, 0};
        int[] dy = {0, 0, -1, 1};
        
        // 使用队列进行 BFS
        Queue<int[]> q = new LinkedList<>();
        q.offer(new int[]{x1, y1});
        visited[x1][y1] = true;
        
        boolean found = false;
        
        while (!q.isEmpty()) {
            int[] current = q.poll();
            int cx = current[0], cy = current[1];
            
            // 如果当前点是终点，设置 found 为 true 并跳出循环
            if (cx == x2 && cy == y2) {
                found = true;
                break;
            }
            
            // 尝试四个方向移动
            for (int i = 0; i < 4; i++) {
                int newX = cx + dx[i];
                int newY = cy + dy[i];
                
                // 检查新位置是否在迷宫范围内，且是通路，且未被访问过
                if (newX >= 0 && newX < n

 && newY >= 0 && newY < m &&
                    maze[newX][newY] == 0 && !visited[newX][newY]) {
                    q.offer(new int[]{newX, newY});
                    visited[newX][newY] = true;
                }
            }
        }
        
        // 根据是否找到终点输出结果
        if (found) {
            System.out.println("YES");
        } else {
            System.out.println("NO");
        }
        
        sc.close();
    }
}
