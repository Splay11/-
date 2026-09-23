#include <iostream>
#include <vector>
using namespace std;

const int maxn = 1010;  // 最大栈大小

int main() {
    vector<long long> stack(maxn, 0);  // 用数组模拟栈
    int top = 0;  // 栈顶指针
    
    // 读取输入
    vector<long long> arr;  // 存储输入的数字
    long long num;
    while (cin >> num) {
        arr.push_back(num);
        // 如果是通过换行符结束输入，可以用下面的判断
        if (cin.get() == '\n') break;
    }
    
    // 遍历输入的每个数
    for (long long x : arr) {
        // 尝试合并栈内元素直到不满足合并条件
        while (true) {
            bool flag = false;  // 用来标记是否执行了合并操作
            long long tmp = 0;  // 用来存储当前连续栈内元素的和
            
            // 从栈顶开始向下遍历所有元素
            for (int i = top; i >= 0; i--) {
                tmp += stack[i];  // 累加栈中的元素
                
                // 如果当前连续元素的和等于当前的x
                if (tmp == x) {
                    // 合并栈内元素，设置新的x值为当前和的两倍
                    x += tmp;
                    // 更新栈顶，i-1表示将合并的元素出栈
                    top = i - 1;
                    flag = true;  // 标记已经合并
                    break;  // 跳出当前for循环
                }
            }
            
            // 如果没有合并任何元素，跳出while循环
            if (!flag) break;
        }
        
        // 将当前x压入栈中
        top++;
        stack[top] = x;
    }
    
    // 输出栈中的所有元素（从栈顶开始打印）
    while (top > 0) {
        cout << stack[top] << " ";
        top--;
    }
    cout << endl;
    
    return 0;
}
