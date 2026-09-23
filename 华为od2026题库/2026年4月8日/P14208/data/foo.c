#include <string.h>
#include <stdlib.h>

/**
 * @param month 要统计的月份（1~12）
 * @param employees 员工姓名数组
 * @param birthdays 员工生日日期数组
 * @param size 数组大小
 * @return 当月应准备的生日礼物数量
 */
int countBirthdayGifts(int month, char** employees, char** birthdays, int size) {
    // 员工数 ≤ 100，用简单数组模拟 name -> 最后录入月份的映射
    char* names[100];
    int months[100];
    int nameCount = 0;

    for (int i = 0; i < size; i++) {
        // 从生日字符串 "YYYY/M/D" 或 "YYYY/MM/DD" 中解析月份
        const char* b = birthdays[i];
        const char* p = b;
        while (*p && *p != '/') p++;   // 跳过年份
        if (!*p) continue;
        p++;                           // 跳过第一个 '/'
        int m = 0;
        while (*p && *p != '/') {
            m = m * 10 + (*p - '0');   // 手动解析月份数字
            p++;
        }

        // 查找该员工是否已有记录
        int found = -1;
        for (int j = 0; j < nameCount; j++) {
            if (strcmp(names[j], employees[i]) == 0) {
                found = j;
                break;
            }
        }
        if (found >= 0) {
            months[found] = m;         // 覆盖为最后一次录入的月份
        } else {
            names[nameCount] = employees[i];
            months[nameCount] = m;
            nameCount++;
        }
    }

    // 统计生日月份等于目标月份的员工数
    int cnt = 0;
    for (int i = 0; i < nameCount; i++) {
        if (months[i] == month) cnt++;
    }
    return cnt;
}
