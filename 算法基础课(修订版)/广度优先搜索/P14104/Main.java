import java.util.*;

public class Main {
    
    // 定义方向向量，分别表示上、下、左、右四个方向
    private static final int[] dx = {-1, 1, 0, 0};
    private static final int[] dy = {0, 0, -1, 1};
    
    public static int shortestPath(int[][] grid, int m, int n, int x1, int y1, int x2, int y2) {
        // 检查起点和终点是否为墙
        if (grid[x1][y1] == 1 || grid[x2][y2] == 1) return -1;
        
        // 创建访问数组，初始化为未访问
        boolean[][] visited = new boolean[m][n];
        
        // 创建队列，队列中存储坐标以及当前路径长度
        Queue<int[]> q = new LinkedList<>();
        q.offer(new int[]{x1, y1, 0});
        visited[x1][y1] = true;
        
        while (!q.isEmpty()) {
            int[] current = q.poll();
            int x = current[0], y = current[1], steps = current[2];
            
            // 如果当前坐标是目标点，返回路径长度
            if (x == x2 && y == y2) {
                return steps;
            }
            
            // 尝试向四个方向移动
            for (int i = 0; i < 4; ++i) {
                int newX = x + dx[i];
                int newY = y + dy[i];
                
                // 检查新坐标是否在范围内，且是空白格子，且未被访问
                if (newX >= 0 && newX < m && newY >= 0 && newY < n 
                    && grid[newX][newY] == 0 && !visited[newX][newY]) {
                    q.offer(new int[]{newX, newY, steps + 1});
                    visited[newX][newY] = true; // 标记为已访问
                }
            }
        }
        
        // 如果队列为空仍未找到目标点，返回 -1
        return -1;
    }
    
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        
        // 读取矩阵的行数和列数
        int m = sc.nextInt();
        int n = sc.nextInt();
        
        // 初始化矩阵
        int[][] grid = new int[m][n];
        for (int i = 0; i < m; ++i) {
            for (int j = 0; j < n; ++j) {
                grid[i][j] = sc.nextInt();
            }
        }
        
        // 读取起点和终点的坐标
        int x1 = sc.nextInt(), y1 = sc.nextInt(), x2 = sc.nextInt(), y2 = sc.nextInt();
        
        // 调用 shortestPath 方法并输出结果
        System.out.println(shortestPath(grid, m, n, x1, y1, x2, y2));
        
        sc.close();
    }
}
