# 产线质检异常批次统计

# 题目内容

产线质检系统对各批次产品进行抽检，系统内记录了每个批次的抽检任务及执行结果。请使用 $MySQL$ $8.0$ 编写 $SQL$ 查询语句，统计 $2026$ 年 $10$ 月 $1$ 日存在质检异常的生产批次。

表名：$inspection\_batches$

| 字段 | 类型 | 说明 |
| ---- | ---- | ---- |
| batch_id | int | 批次 ID |
| prod_line | varchar($20$) | 产线编码 |
| batch_date | date | 批次日期 |

表名：$inspection\_tasks$

| 字段 | 类型 | 说明 |
| ---- | ---- | ---- |
| inspect_id | int | 抽检任务 ID |
| batch_id | int | 批次 ID |
| plan_cnt | int | 计划抽检数量 |
| actual_cnt | int | 实际抽检数量 |
| inspect_status | varchar($20$) | 抽检状态，取值包括 PASS、TODO、ING |

质检异常任务指未合格的任务，或实际抽检数量少于计划抽检数量的任务。请输出存在至少 $1$ 个异常任务的批次。
输出字段固定为：$prod\_line$、$batch\_id$、$task\_cnt$、$abnormal\_cnt$、$shortfall$。列名和列顺序必须与要求一致。

其中 $task\_cnt$ 表示该批次的抽检任务总数；$abnormal\_cnt$ 表示异常任务数量；$shortfall$ 表示该批次中所有少检数量之和，未少检的任务不计入少检数量。

结果先按 $abnormal\_cnt$ 降序排列；若相同，按 $shortfall$ 降序排列；若相同，按 $prod\_line$ 升序排列；若仍相同，按 $batch\_id$ 升序排列。



## 样例1



**输入**



```sql
CREATE TABLE inspection_batches (
batch_id int,
prod_line varchar(20),
batch_date date
);

CREATE TABLE inspection_tasks (
inspect_id int,
batch_id int,
plan_cnt int,
actual_cnt int,
inspect_status varchar(20)
);

INSERT INTO inspection_batches VALUES
(201, 'A01', '2026-10-01'),
(202, 'A01', '2026-10-01'),
(203, 'B01', '2026-10-01'),
(204, 'A01', '2026-09-30');

INSERT INTO inspection_tasks VALUES
(1, 201, 12, 12, 'PASS'),
(2, 201, 9, 4, 'PASS'),
(3, 201, 7, 7, 'TODO'),
(4, 202, 6, 6, 'PASS'),
(5, 202, 5, 5, 'PASS'),
(6, 203, 10, 2, 'TODO'),
(7, 203, 8, 8, 'PASS');
```



**输出**


| prod_line | batch_id | task_cnt | abnormal_cnt | shortfall |
| ---- | ---- | ---- | ---- | ---- |
| A01 | 201 | 3 | 2 | 5 |
| B01 | 203 | 2 | 1 | 8 |




**说明**

$batch\_id=201$ 任务：

任务 $1$：$PASS，plan=12$ $actual=12$，正常；

任务 $2$：$PASS，plan=9$ $actual=4$，实际少于计划，异常，少检 $9-4=5$；

任务 $3$：$TODO$ 未合格，异常，无少检数量；
总 $task\_cnt=3$，$abnormal\_cnt=2$，$shortfall=5$。

$batch\_id=203$ 任务：

任务 $6$：$TODO$ 未合格，$plan=10$ $actual=2$，异常，少检 $10-2=8$；

任务 $7$：$PASS，plan=8$ $actual=8$ 正常；
$task\_cnt=2$，$abnormal\_cnt=1$，$shortfall=8$。

$batch\_id=202$ 全部任务正常，不输出。

$batch\_id=204$ 批次日期为 $2026$ 年 $9$ 月 $30$ 日，不在统计范围内，不输出。


## 样例2



**输入**



```sql
CREATE TABLE inspection_batches (
batch_id int,
prod_line varchar(20),
batch_date date
);

CREATE TABLE inspection_tasks (
inspect_id int,
batch_id int,
plan_cnt int,
actual_cnt int,
inspect_status varchar(20)
);

INSERT INTO inspection_batches VALUES
(301, 'C01', '2026-10-01'),
(302, 'C01', '2026-10-01');

INSERT INTO inspection_tasks VALUES
(11, 301, 10, 8, 'PASS'),
(12, 301, 6, 6, 'ING'),
(13, 302, 4, 4, 'PASS'),
(14, 302, 7, 7, 'PASS');
```



**输出**


| prod_line | batch_id | task_cnt | abnormal_cnt | shortfall |
| ---- | ---- | ---- | ---- | ---- |
| C01 | 301 | 2 | 2 | 2 |




**说明**

$batch\_id=301$ 任务：

任务 $11$：$PASS，plan=10$ $actual=8$，实际少于计划，异常，少检 $10-8=2$；

任务 $12$：$ING$ 未合格，异常，无少检数量；
$task\_cnt=2$，$abnormal\_cnt=2$，$shortfall=2$。

$batch\_id=302$ 两个任务均合格且数量达标，无异常，不输出。



注：不需要考虑输入异常情况。
