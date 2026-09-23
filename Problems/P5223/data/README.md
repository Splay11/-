# P5223 数据说明

共 10 个测试点。前 8 个为小数据，后 2 个为大数据（m 较大、答案需取模）。

| 编号 | 组名 | m | 说明 |
|------|------|---|------|
| 1 | g01 | 2 | sample1-m=2 |
| 2 | g02 | 3 | sample2-m=3 |
| 3 | g03 | 1 | boundary-min-m=1 |
| 4 | g04 | 4 | small-m=4 |
| 5 | g05 | 5 | small-m=5 |
| 6 | g06 | 6 | small-m=6 |
| 7 | g07 | 7 | small-m=7 |
| 8 | g08 | 8 | small-m=8 |
| 9 | g09 | 10 | large-m=10 |
| 10 | g10 | 12 | max-boundary-m=12 |

## 预计易错

- 忘记对 998244353 取模
- 直接计算 `2**(2**m - 1)` 导致溢出
- C++ 中用 `int`/`unsigned int` 计算指数时溢出（`1<<12=4096` 在 int 内安全，但指数 `(1<<12)-1=4095` 作为幂次传给倍增运算时，迭代次数需要 `long long` 来计数——不过 4095 次循环即使暴力也能过，但 `1<<m` 在 m=12 时对 int 是安全的，对 long long 封装依然安全。）

## 对拍方式

```bash
# 生成数据
python gen.py
# C++ 标程验证
g++ std.cpp -o std.exe -O2 -std=c++17
for f in data/testcaseg*.in; do ./std.exe < $f | diff - ${f%.in}.out; done
# Java 标程验证
javac Main.java
for f in data/testcaseg*.in; do java Main < $f | diff - ${f%.in}.out; done
```