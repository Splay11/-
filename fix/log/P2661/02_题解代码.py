## 题解

## 题面描述

小红为了区分机器人与真实用户，在每张 5×5 的验证码图片里放置了一些“#”和数字（0~9）。  
- 机器人往往只会识别数字（把“#”当作噪声），从而得到一串无意义的数字。  
- 我们要根据“#”的排布形态来判断，这张 5×5 图片实际上代表哪个数字（0~9）。


## 二、思路解析

1. **核心：模板匹配**  
   - 题目给定（或自行定义）的 0~9 的 5×5 “#” 排布各不相同，可以用作“模板”。  
   - 每张图片中的‘0’~‘9’其实是干扰，真正要看的只是“#”的分布位置。  

2. **实现步骤**  
   1. **初始化模板**：将 0~9 的 5×5 图案（使用“#”和“.”）硬编码到一个数组/向量中。  
      - 其中 “#” 表示此位置应该是“#”；  
      - “.” 表示此位置可以是任意数字或空白（在代码里，我们用数字替换成“.”来对比）。  
   2. **读入数据并分块**：  
      - 读入 $m$，再读入 $5m$ 行；  
      - 每 5 行构成一张 5×5 图片，存储到 `pictures[i]`。  
   3. **预处理**：  
      - 对每张图片里的每个字符，如果是‘0’~‘9’，就改为‘.’；如果是‘#’，就保留。  
   4. **匹配识别**：  
      - 把预处理后的 5×5 与事先定义好的 10 个模板（digitPatterns[0..9]）一一比较；  
      - 如果某个模板的 5 行都完全一致，则说明这是那个数字。  
   5. **输出结果**：  
      - 将识别到的数字依次拼起来，最后一次性输出。  

## cpp
```cpp
#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int m;
    cin >> m;  // 读入图片张数

    // 准备一个二维数组 digitPatterns[digit][row] = string(5列)
    // 用来存储 0~9 每个数字对应的 5×5 模板（仅含 '#' 和 '.'）
    vector<vector<string>> digitPatterns(10, vector<string>(5));

    // 下面填充每个数字的 5行图案（与前面列出的示例保持一致）
    // digit=0
    digitPatterns[0] = {
        "#...#",
        "#.#.#",
        "#.#.#",
        "#.#.#",
        "#...#"
    };

    // digit=1  (题目示例)
    digitPatterns[1] = {
        "##.##",
        "##.##",
        "##.##",
        "##.##",
        "##.##"
    };

    // digit=2
    digitPatterns[2] = {
        "#...#",
        "###.#",
        "#...#",
        "#.###",
        "#...#"
    };

    // digit=3
    digitPatterns[3] = {
        "#...#",
        "###.#",
        "#...#",
        "###.#",
        "#...#"
    };

    // digit=4
    digitPatterns[4] = {
        "#.#.#",
        "#.#.#",
        "#...#",
        "###.#",
        "###.#"
    };

    // digit=5  (题目示例)
    digitPatterns[5] = {
        "#...#",
        "#.###",
        "#...#",
        "###.#",
        "#...#"
    };

    // digit=6
    digitPatterns[6] = {
        "#...#",
        "#.###",
        "#...#",
        "#.#.#",
        "#...#"
    };

    // digit=7
    digitPatterns[7] = {
        "#...#",
        "###.#",
        "###.#",
        "###.#",
        "###.#"
    };

    // digit=8
    digitPatterns[8] = {
        "#...#",
        "#.#.#",
        "#...#",
        "#.#.#",
        "#...#"
    };

    // digit=9
    digitPatterns[9] = {
        "#...#",
        "#.#.#",
        "#...#",
        "###.#",
        "#...#"
    };

    // 一次性把输入的 m*5 行读入
    // 每 5 行构成一张图片
    vector<vector<string>> pictures(m, vector<string>(5));
    for(int i = 0; i < m; i++){
        for(int r = 0; r < 5; r++){
            string line;
            cin >> line;  // 读这一行
            pictures[i][r] = line;
        }
    }

    // 用来拼接最终结果的字符串
    string result;
    result.reserve(m);

    // 逐张识别
    for(int i = 0; i < m; i++){
        // 先把 pictures[i] 中所有的数字字符(0~9)改成 '.'
        for(int r = 0; r < 5; r++){
            for(int c = 0; c < 5; c++){
                if(isdigit(pictures[i][r][c])){
                    pictures[i][r][c] = '.';
                }
            }
        }

        // 与 digitPatterns[0..9] 逐一比对
        int recognizedDigit = -1;
        for(int d = 0; d < 10; d++){
            bool match = true;
            for(int r = 0; r < 5; r++){
                if(pictures[i][r] != digitPatterns[d][r]){
                    match = false;
                    break;
                }
            }
            if(match){
                recognizedDigit = d;
                break;
            }
        }

        // 题目保证一定能匹配到，这里做个容错
        if(recognizedDigit == -1){
            recognizedDigit = 0; 
        }

        // 加入结果
        result.push_back(char('0' + recognizedDigit));
    }

    // 输出完整结果
    cout << result << "\n";
    return 0;
}

```
## python
```python
def main():
    import sys
    input = sys.stdin.readline

    # 读入图片张数
    m = int(input().strip())

    # 定义 0~9 各个数字对应的 5×5 模板
    digitPatterns = [
        [
            "#...#",
            "#.#.#",
            "#.#.#",
            "#.#.#",
            "#...#"
        ],
        [
            "##.##",
            "##.##",
            "##.##",
            "##.##",
            "##.##"
        ],
        [
            "#...#",
            "###.#",
            "#...#",
            "#.###",
            "#...#"
        ],
        [
            "#...#",
            "###.#",
            "#...#",
            "###.#",
            "#...#"
        ],
        [
            "#.#.#",
            "#.#.#",
            "#...#",
            "###.#",
            "###.#"
        ],
        [
            "#...#",
            "#.###",
            "#...#",
            "###.#",
            "#...#"
        ],
        [
            "#...#",
            "#.###",
            "#...#",
            "#.#.#",
            "#...#"
        ],
        [
            "#...#",
            "###.#",
            "###.#",
            "###.#",
            "###.#"
        ],
        [
            "#...#",
            "#.#.#",
            "#...#",
            "#.#.#",
            "#...#"
        ],
        [
            "#...#",
            "#.#.#",
            "#...#",
            "###.#",
            "#...#"
        ]
    ]
    
    # 读取 m 张图片，每张图片有 5 行
    pictures = []
    for _ in range(m):
        pic = [input().strip() for _ in range(5)]
        pictures.append(pic)
    
    result = []
    # 逐张识别
    for pic in pictures:
        # 将每张图片中所有数字字符替换成 '.'
        new_pic = []
        for line in pic:
            new_line = ''.join('.' if ch.isdigit() else ch for ch in line)
            new_pic.append(new_line)
        
        recognizedDigit = -1
        # 与预设的数字模板逐一比对
        for d in range(10):
            if new_pic == digitPatterns[d]:
                recognizedDigit = d
                break
        if recognizedDigit == -1:
            recognizedDigit = 0  # 容错处理
        result.append(str(recognizedDigit))
    
    # 输出最终结果
    print("".join(result))

if __name__ == '__main__':
    main()

```
## java
```java
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        
        // 读入图片张数
        int m = sc.nextInt();
        
        // 定义 0~9 各个数字对应的 5×5 模板
        String[][] digitPatterns = new String[10][5];
        
        digitPatterns[0] = new String[] {
            "#...#",
            "#.#.#",
            "#.#.#",
            "#.#.#",
            "#...#"
        };
        digitPatterns[1] = new String[] {
            "##.##",
            "##.##",
            "##.##",
            "##.##",
            "##.##"
        };
        digitPatterns[2] = new String[] {
            "#...#",
            "###.#",
            "#...#",
            "#.###",
            "#...#"
        };
        digitPatterns[3] = new String[] {
            "#...#",
            "###.#",
            "#...#",
            "###.#",
            "#...#"
        };
        digitPatterns[4] = new String[] {
            "#.#.#",
            "#.#.#",
            "#...#",
            "###.#",
            "###.#"
        };
        digitPatterns[5] = new String[] {
            "#...#",
            "#.###",
            "#...#",
            "###.#",
            "#...#"
        };
        digitPatterns[6] = new String[] {
            "#...#",
            "#.###",
            "#...#",
            "#.#.#",
            "#...#"
        };
        digitPatterns[7] = new String[] {
            "#...#",
            "###.#",
            "###.#",
            "###.#",
            "###.#"
        };
        digitPatterns[8] = new String[] {
            "#...#",
            "#.#.#",
            "#...#",
            "#.#.#",
            "#...#"
        };
        digitPatterns[9] = new String[] {
            "#...#",
            "#.#.#",
            "#...#",
            "###.#",
            "#...#"
        };

        // 读取 m 张图片，每张图片有 5 行（使用 sc.next() 逐个读取，不包含空格）
        String[][] pictures = new String[m][5];
        for (int i = 0; i < m; i++) {
            for (int r = 0; r < 5; r++) {
                pictures[i][r] = sc.next();
            }
        }
        
        StringBuilder result = new StringBuilder();
        // 逐张识别
        for (int i = 0; i < m; i++) {
            // 替换图片中所有数字字符为 '.'
            String[] pic = new String[5];
            for (int r = 0; r < 5; r++) {
                StringBuilder sb = new StringBuilder();
                for (int c = 0; c < 5; c++) {
                    char ch = pictures[i][r].charAt(c);
                    if (Character.isDigit(ch)) {
                        sb.append('.');
                    } else {
                        sb.append(ch);
                    }
                }
                pic[r] = sb.toString();
            }
            
            int recognizedDigit = -1;
            // 逐一比对数字模板
            for (int d = 0; d < 10; d++) {
                boolean match = true;
                for (int r = 0; r < 5; r++) {
                    if (!pic[r].equals(digitPatterns[d][r])) {
                        match = false;
                        break;
                    }
                }
                if (match) {
                    recognizedDigit = d;
                    break;
                }
            }
            if (recognizedDigit == -1) {
                recognizedDigit = 0; // 容错处理
            }
            result.append(recognizedDigit);
        }
        
        // 输出最终结果
        System.out.println(result.toString());
        sc.close();
    }
}

```