1.安装skills

将./.cursor下的skills 中的所有依赖的skills安装到cursor中，以便在agent中`/`使用


2.skills介绍

- **algorithm-contest-problemsetter**：算法竞赛出题框架。用于设计/改题、题面与数据范围、部分分、测试与生成器思路、题解与标程规划；不负责最终验题与 hack。

- **codefun2000-problem-generator**：出题工作流。从 CodeFun2000 题目或本地题面拉题并生成出题工作区（题面、标程、题解、数据、校验流程）；有 pid 时走抓取，也可只贴题面或用户提供标程/题解。

prompt用法：

case1:无题解无std
```
/codefun2000-problem-generator  在@Problems 文件夹下，出题，pid: P4000

std+题解+数据的出题框架请参考：/algorithm-contest-problemsetter
```


case2:给定题面
```
/codefun2000-problem-generator  在@Problems 文件夹下，出题，题面在@xxx 中

std+题解+数据的出题框架请参考：/algorithm-contest-problemsetter
```


case3:给定std
```
/codefun2000-problem-generator  在@Problems 文件夹下，出题，根据@std.py 来出题

std+题解+数据的出题框架请参考：/algorithm-contest-problemsetter
```


- **codefun2000-problem-uploader**：上传OJ工作流。通过本地 `utils` 脚本向 CodeFun2000 上传题解、测试数据或提交标程；缺环境/脚本/参数时会明确报错并停止。


prompt用法：

case1:数据+题解一起上传
```
/codefun2000-problem-uploader  将@xxx/P4000 上传
```


case2:只上传数据
```
/codefun2000-problem-uploader  将@xxx/P4000/data 中的数据上传
```

"# problem-maker" 
