# 题解

## 题面描述

给定一个正整数 $n$，求满足以下条件的三元组 $(a,b,c)$ 的数量：

- $a+b+c=n$。  
- $a,b,c$ 是两两不同的正整数。  
- $a,b,c$ 的各个数位均不包含数字 $2$ 和 $4$。  

若通过改变三个正整数的顺序可以得到相同的组合，则只计算为一种分解方法。

---

## 思路

1. **定义“好数”**  
   令  
   ![image](/file/2/f5kyE1a-9XD_kLWWCA62C.png) 

2. **生成函数**  
   构造  
   $$
   G(x)=\sum_{i=0}^{\infty}f[i]\,x^i.
   $$

3. **容斥计数**  
   - 令 $E_1[n]$ 为 $G(x)^3$ 在 $x^n$ 项的系数，对应“有序三元组（允许相等）”的数量。  
   - 令 $E_2[n]$ 为 $G(x)\cdot G(x^2)$ 在 $x^n$ 项的系数，对应恰有一对相等（如 $a=b\neq c$）的有序三元组数量。  
   - 令  
     ![image](/file/2/dgg41i5tRZYg6QXZuScT6.png) 
   根据容斥原理，有序且互异的三元组数量为  
   $$
   E_1[n]\;-\;3E_2[n]\;+\;2E_3[n].
   $$

4. **去重**  
   有序互异三元组一共有 $E_1[n]-3E_2[n]+2E_3[n]$ 种，不考虑顺序的无序三元组要除以 $3! = 6$，即  
   $$
   \frac{E_1[n]-3E_2[n]+2E_3[n]}{6}.
   $$

5. **FFT 卷积**  
   - 直接构造长度不小于 $3n$ 的数组，分别存放 $f[i]$ 和 $f[i]$ “跳步”版（用于计算 $E_2$）。  
   - 通过 FFT/逆 FFT 快速得到 $E_1$ 和 $E_2$，再按上面公式计算即可。

---

## C++

```cpp
#include <bits/stdc++.h>
using namespace std;
using cd = complex<double>;

// FFT 变换，自底向上实现
void fft(vector<cd>& a, bool inv){
    int n = a.size(), j = 0;
    // 位反转置换
    for(int i = 1; i < n; ++i){
        int bit = n >> 1;
        for(; j & bit; bit >>= 1) j ^= bit;
        j |= bit;
        if(i < j) swap(a[i], a[j]);
    }
    const double PI = acos(-1);
    // 迭代合并
    for(int len = 2; len <= n; len <<= 1){
        double ang = 2 * PI / len * (inv ? -1 : 1);
        cd wlen(cos(ang), sin(ang));
        for(int i = 0; i < n; i += len){
            cd w(1);
            for(int j = 0; j < len/2; ++j){
                cd u = a[i+j];
                cd v = a[i+j+len/2] * w;
                a[i+j] = u + v;
                a[i+j+len/2] = u - v;
                w *= wlen;
            }
        }
    }
    if(inv){
        // 逆变换需除以 n
        for(cd& x : a) x /= n;
    }
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    vector<int> qs(T);
    int mx = 0;
    for(int i = 0; i < T; ++i){
        cin >> qs[i];
        mx = max(mx, qs[i]);
    }

    // 标记好数
    vector<char> good(mx+1, 0);
    for(int i = 1; i <= mx; ++i){
        int x = i;
        bool ok = true;
        while(x){
            int d = x % 10;
            if(d == 2 || d == 4){
                ok = false;
                break;
            }
            x /= 10;
        }
        good[i] = ok;
    }

    // 计算 FFT 所需的长度
    int lim = 1;
    while(lim < 3*mx + 1) lim <<= 1;

    vector<cd> A(lim), B(lim);
    // A[i]=1 表示 f[i]=1，B[2*i]=1 表示 f[i]=1
    for(int i = 0; i <= mx; ++i){
        if(good[i]){
            A[i] = 1;
            B[2*i] = 1;
        }
    }

    // FFT 变换
    fft(A, false);
    fft(B, false);

    vector<long long> E1(mx+1), E2(mx+1);
    // 计算 E1 = A*A*A
    {
        vector<cd> F = A;
        for(int i = 0; i < lim; ++i) F[i] *= F[i] * A[i];
        fft(F, true);
        for(int i = 0; i <= mx; ++i)
            E1[i] = llround(F[i].real());
    }
    // 计算 E2 = A*B
    {
        vector<cd> F = A;
        for(int i = 0; i < lim; ++i) F[i] *= B[i];
        fft(F, true);
        for(int i = 0; i <= mx; ++i)
            E2[i] = llround(F[i].real());
    }

    // 计算最终答案并输出
    for(int n : qs){
        long long e3 = (n % 3 == 0 && good[n/3]) ? 1 : 0;
        long long tot = E1[n] - 3*E2[n] + 2*e3;
        cout << (tot / 6) << "\n";
    }
    return 0;
}
```
## Python

```python
import sys
import threading
import numpy as np

def main():
    input = sys.stdin.readline
    T = int(input().strip())
    qs = [int(input().strip()) for _ in range(T)]
    mx = max(qs)

    # 标记好数
    good = np.zeros(mx+1, dtype=int)
    for i in range(1, mx+1):
        x = i
        ok = True
        while x > 0:
            d = x % 10
            if d == 2 or d == 4:
                ok = False
                break
            x //= 10
        good[i] = ok

    # 构造多项式系数
    lim = 1
    while lim < 3*mx + 1:
        lim <<= 1

    A = np.zeros(lim, dtype=np.int64)
    B = np.zeros(lim, dtype=np.int64)
    A[:mx+1] = good
    B[:2*mx+1:2] = good

    # FFT 计算卷积
    FA = np.fft.rfft(A)
    FB = np.fft.rfft(B)

    # E1 = A*A*A
    E1 = np.fft.irfft(FA * FA * FA, n=lim).round().astype(np.int64)[:mx+1]
    # E2 = A*B
    E2 = np.fft.irfft(FA * FB, n=lim).round().astype(np.int64)[:mx+1]

    # 计算答案
    ans = [0] * (mx+1)
    for n in range(mx+1):
        e3 = 1 if n % 3 == 0 and good[n//3] == 1 else 0
        tot = E1[n] - 3 * E2[n] + 2 * e3
        ans[n] = tot // 6

    # 输出结果
    print("\n".join(str(ans[q]) for q in qs))

if __name__ == "__main__":
    threading.Thread(target=main).start()
```
## Java

```java
import java.util.*;

public class Main {
    // 定义复数类，用于存储和操作复数
    static class Complex {
        double real, imag;

        Complex(double real, double imag) {
            this.real = real;
            this.imag = imag;
        }

        // 复数加法
        Complex add(Complex other) {
            return new Complex(this.real + other.real, this.imag + other.imag);
        }

        // 复数减法
        Complex subtract(Complex other) {
            return new Complex(this.real - other.real, this.imag - other.imag);
        }

        // 复数乘法
        Complex multiply(Complex other) {
            return new Complex(this.real * other.real - this.imag * other.imag,
                    this.imag * other.real + this.real * other.imag);
        }

        // 复数除法
        Complex divide(double scalar) {
            return new Complex(this.real / scalar, this.imag / scalar);
        }

        // 获取复数的实部
        double real() {
            return this.real;
        }
    }

    // 自底向上的FFT变换
    static void fft(List<Complex> a, boolean inv) {
        int n = a.size(), j = 0;
        // 位反转置换
        for (int i = 1; i < n; ++i) {
            int bit = n >> 1;
            for (; (j & bit) != 0; bit >>= 1) j ^= bit;
            j |= bit;
            if (i < j) Collections.swap(a, i, j); // 交换元素
        }
        final double PI = Math.acos(-1);
        // 迭代合并过程
        for (int len = 2; len <= n; len <<= 1) {
            double ang = 2 * PI / len * (inv ? -1 : 1); // 计算旋转因子角度
            Complex wlen = new Complex(Math.cos(ang), Math.sin(ang)); // 计算旋转因子
            for (int i = 0; i < n; i += len) {
                Complex w = new Complex(1, 0);
                // 逐步合并子问题
                for (int k = 0; k < len / 2; ++k) {  // 内部循环变量改名为 k
                    Complex u = a.get(i + k);
                    Complex v = a.get(i + k + len / 2).multiply(w);
                    a.set(i + k, u.add(v)); // 更新结果
                    a.set(i + k + len / 2, u.subtract(v)); // 更新结果
                    w = w.multiply(wlen); // 更新旋转因子
                }
            }
        }
        if (inv) {
            // 如果是逆变换，需要除以n
            for (int i = 0; i < n; ++i) {
                a.set(i, a.get(i).divide(n));
            }
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // 读取测试案例数
        int T = sc.nextInt();
        int[] qs = new int[T];
        int mx = 0;
        // 读取每个测试案例
        for (int i = 0; i < T; ++i) {
            qs[i] = sc.nextInt();
            mx = Math.max(mx, qs[i]); // 更新最大值
        }

        // 标记"好数"，即不包含2或4的数字
        boolean[] good = new boolean[mx + 1];
        for (int i = 1; i <= mx; ++i) {
            int x = i;
            boolean ok = true;
            while (x > 0) {
                int d = x % 10;
                if (d == 2 || d == 4) {
                    ok = false;
                    break;
                }
                x /= 10;
            }
            good[i] = ok; // 标记为好数
        }

        // 计算FFT需要的大小
        int lim = 1;
        while (lim < 3 * mx + 1) lim <<= 1;

        // 创建FFT的输入数据
        List<Complex> A = new ArrayList<>(Collections.nCopies(lim, new Complex(0, 0)));
        List<Complex> B = new ArrayList<>(Collections.nCopies(lim, new Complex(0, 0)));

        // 初始化A和B，A[i] = 1表示f[i] = 1，B[2 * i] = 1表示f[i] = 1
        for (int i = 0; i <= mx; ++i) {
            if (good[i]) {
                A.set(i, new Complex(1, 0));
                B.set(2 * i, new Complex(1, 0));
            }
        }

        // 进行FFT变换
        fft(A, false);
        fft(B, false);

        // 存储E1和E2的结果
        long[] E1 = new long[mx + 1];
        long[] E2 = new long[mx + 1];

        // 计算 E1 = A * A * A
        {
            List<Complex> F = new ArrayList<>(A);
            for (int i = 0; i < lim; ++i) {
                F.set(i, F.get(i).multiply(F.get(i)).multiply(A.get(i)));
            }
            fft(F, true);
            for (int i = 0; i <= mx; ++i) {
                E1[i] = Math.round(F.get(i).real()); // 取实部并转换为long型
            }
        }

        // 计算 E2 = A * B
        {
            List<Complex> F = new ArrayList<>(A);
            for (int i = 0; i < lim; ++i) {
                F.set(i, F.get(i).multiply(B.get(i)));
            }
            fft(F, true);
            for (int i = 0; i <= mx; ++i) {
                E2[i] = Math.round(F.get(i).real()); // 取实部并转换为long型
            }
        }

        // 根据查询计算最终答案并输出
        for (int n : qs) {
            long e3 = (n % 3 == 0 && good[n / 3]) ? 1 : 0;
            long tot = E1[n] - 3 * E2[n] + 2 * e3;
            System.out.println(tot / 6); // 输出最终结果
        }

        sc.close(); // 关闭Scanner
    }
}
```