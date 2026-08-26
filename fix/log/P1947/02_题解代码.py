## 思路
对于加减乘除四种都可以正常模拟，对于乘方，由于数太大。对两边同时取对数, log_10(a^b) = b * log_10(a) .  log_10(b^a) = a * log_10(b) , 直接比较后者即可。

这里注意，取对数的时候如果a 或者 b = 0 , 那么可能造成除0错误，所以特判这两种情况。

## 代码

### python
```python
import math
t = int(input())
# 比较两个数的大小 , 返回 = , > , <
def check (x , y):
    if x == y:
        return "="
    elif x > y:
        return ">"
    return "<"
for _ in range(t):
    a , b , op = input().split()
    a , b = int(a) , int(b)
    if op == "+":
        print(check(a + b, b + a))
    elif op == "-":
        print(check(a - b, b - a))
    elif op == "*":
        print(check(a * b, b * a))
    elif op == "/":
        print(check(a / b, b / a))
    else:
        # 准备使用10为底，但是考虑a,b等于1的情况，这种是除0错误
        if a == 1:
            x = 1
            y = b
        elif b == 1:
            x = a
            y = 1
        else:
            x = b * math.log(10 , a) # 利用换底公式,a^b = b * log(a)
            y = a * math.log(10 , b) # 利用换底公式,b^a = a * log(b)
        print(check(x , y))
```

### Java
```Java
import java.util.*;
/**第二题次方运算超过double，可以使用log的换底公式呀，唉，可惜*/
public class Main {
    public static void main(String[] args) {
        Scanner in =new Scanner(System.in);
        int t=in.nextInt();
        for(int i=0;i<t;i++){
            int a=in.nextInt();
            int b=in.nextInt();
            String s=in.next();
            if(s.equals("+")||s.equals("*")) System.out.println("=");
            if(s.equals("/")||s.equals("-")){
                if(a==b) System.out.println("=");
                else if(a>b) System.out.println(">");
                else if(a<b) System.out.println("<");
            }
            if(s.equals("^")){
                if(a==1){
                    if(b>1) System.out.println("<");
                    else System.out.println("=");
                }else if(b==1){
                    System.out.println(">");
                }else{
                    double a_b =b*Math.log10(a);
                    double b_a=a*Math.log10(b);
                    if(a_b==b_a) System.out.println("=");
                    else if(a_b>b_a) System.out.println(">");
                    else if(b_a>a_b) System.out.println("<");
                }
            }

        }
    }

}
```

### C++
```C++
#include <iostream>
#include <algorithm>
#include <cmath>

using namespace std;
typedef long long LL;

char check(LL a, LL b)
{
	if (a > b)
		return '>';
	else if (a < b)
		return '<';
	return '=';
}

int main()
{
	int T;
	cin >> T;
	while (T--)
	{
		LL a, b;
		char op;
		scanf("%lld %lld %c", &a, &b, &op);
		switch (op)
		{
			case '+':
				cout << '=' << endl;
                break;
			case '-':
				cout << check(a - b, b - a) << endl;
                break;
			case '*':
				cout << '=' << endl;
                break;
			case '/':
				cout << check(a / b, b / a) << endl;
                break;
			case '^':
				double x = (double)b * log10(a);
				double y = (double)a * log10(b);
				if (x > y)
					cout << '>' << endl;
				else if (x < y)
					cout << '<' << endl;
				else cout << '=' << endl;
                break;
		}

	}
	return 0;
}
```
OJ会员可以通过点击题目上方《已通过》查看其他通过代码来学习。