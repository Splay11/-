## 题解
简单的时间转换，将当前时间减8h就是结果。

## AC代码

- Python
```python
def convert_time(time_str):
    h, m = map(int, time_str.split(':'))
    total_min = h * 60 + m - 8 * 60
    if total_min < 0:
        total_min += 24 * 60
    new_h = total_min // 60
    new_m = total_min % 60
    return f"{new_h:02d}:{new_m:02d}"


t = int(input().strip())
results = [convert_time(input().strip()) for _ in range(t)]
print('\n'.join(results))

```
- Java
```java
import java.util.Scanner;

public class Main {
    public static String convertTime(String timeStr) {
        String[] parts = timeStr.split(":");
        int h = Integer.parseInt(parts[0]);
        int m = Integer.parseInt(parts[1]);
        int totalMin = h * 60 + m - 8 * 60;
        if (totalMin < 0) {
            totalMin += 24 * 60;
        }
        int newH = totalMin / 60;
        int newM = totalMin % 60;
        return String.format("%02d:%02d", newH, newM);
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int t = scanner.nextInt();
        scanner.nextLine(); 
        String[] results = new String[t];
        for (int i = 0; i < t; i++) {
            String timeStr = scanner.nextLine();
            results[i] = convertTime(timeStr);
        }
        for (String result : results) {
            System.out.println(result);
        }
    }
}

```

- CPP
```cpp
#include <iostream>
#include <vector>
#include <cstdio>
#include <iomanip>

using namespace std;

string convertTime(const string& timeStr) {
    int h, m;
    sscanf(timeStr.c_str(), "%d:%d", &h, &m);
    int totalMin = h * 60 + m - 8 * 60;
    if (totalMin < 0) {
        totalMin += 24 * 60;
    }
    int newH = totalMin / 60;
    int newM = totalMin % 60;
    char buffer[6];
    snprintf(buffer, sizeof(buffer), "%02d:%02d", newH, newM);
    return string(buffer);
}

int main() {
    int t;
    cin >> t;
    vector<string> results(t);
    string timeStr;
    for (int i = 0; i < t; ++i) {
        cin >> timeStr;
        results[i] = convertTime(timeStr);
    }
    for (const auto& result : results) {
        cout << result << endl;
    }
    return 0;
}

```