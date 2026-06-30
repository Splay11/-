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

prompt用法（LeetCode 模式）：

case1:无题解无std
```
/leetcode-core-code-mode 在 @Pxxxx 下出题，出题的 pid: Pxxxx，根据题意写清接口与题面；题目根下放 `gen.py` 等，**`compile.sh`、`config.yaml`、`template.*`、`user.*` 与测例一并放在 `data/`**（`compile.sh` 从仓库根 `problem-maker/compile.sh` 原样拷入 `data/`）
```


case2:给定 std
```
/leetcode-core-code-mode 在 @Problems/P4000 下对齐：以 @std.cpp（或 std.py / Main.java）为权威实现，统一三语言 user 桩签名，重写 template 读入与调用，补齐题解、造数；**`compile.sh` / `config.yaml` / `template.*` / `user.*` 均落在 `data/`**
```



- **codefun2000-problem-uploader**：上传 OJ 工作流。通过本地 `utils` 脚本向 CodeFun2000 上传题解、测试数据、提交标程；**核心代码模式**下 **`compile.sh` 等与测例同在 `data/`** 时，一次 `upload_testdata.py` 即可带上；另可生成 `leetcode_core_bundle_paths.json`（扫描 `data/` 内约定名）供扩展上传（详见 `utils/README.md`）；缺环境/脚本/参数时会明确报错并停止。


prompt用法：

case1:数据+题解一起上传
```
/codefun2000-problem-uploader  将@xxx/P4000 上传
```


case2:只上传数据
```
/codefun2000-problem-uploader  将@xxx/P4000/data 中的数据上传
```


case3:LeetCode 模式整套（题解 + 数据 + 后台文件）
```
/codefun2000-problem-uploader 将 @Problems/P4000 整套上传（测例与 **位于 `data/` 的** compile.sh、config.yaml、template.*、user.* 等由 `upload_testdata.py` 一并上传）
```

