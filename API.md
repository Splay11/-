# API 外部调用使用说明

本文档说明 `api` 插件注册的全部对外接口（含题目 API 与题目压缩包导入导出）。接口路径均以 HydroOJ 站点根地址为前缀，例如：

```text
https://codefun2000.com/api/problem/detail
```

控制面板「题目压缩包」页（`/manage/problem-zip`）仍由 `ProblemZip` 插件提供，页面通过会话调用同一组 `/api/problem-zip/*` 接口。

## 通用约定

- 返回格式：默认返回 JSON；部分导出接口直接返回 zip 文件流。
- **鉴权**：题目类 `/api/problem*` 接口只认站点级秘钥。
- `/api/problem-zip/*` 为双通道：已登录且具备 `PRIV_EDIT_SYSTEM` 的管理员可用会话 cookie；外部调用方必须带同一把站点秘钥。
- 秘钥读取顺序：`X-Api-Key` → `Authorization: Bearer <key>` → query/body 的 `apiKey`。
- 秘钥仅在控制面板 **对外 API 秘钥** 页（`/manage/external-api`）对系统管理员可见；轮换后旧钥立即失效。
- 过期或错误一律 `401`，响应 `{ "message": "Permission denied." }`。
- `domainId`：HydroOJ 域 ID。题目类接口从 query/body 读取；压缩包接口使用当前 Hydro 域（默认域，或用 `/d/<domainId>/api/problem-zip/...` 指定）。
- `pid`：题目编号，例如 `P1001`。
- `psid`：题单在 MongoDB 中的 ObjectId 字符串。

`submit_proxy` 仍可传 `uname`/`password`，那是「以谁的身份去 Hydro 交题」，不是接口鉴权；该接口本身必须先过秘钥。

### 鉴权示例

```bash
# 推荐：请求头
curl "https://codefun2000.com/api/problem/detail?domainId=system&pid=P1001" \
  -H "X-Api-Key: $CF_API_KEY"

# 等价：Bearer
curl "https://codefun2000.com/api/problem/detail?domainId=system&pid=P1001" \
  -H "Authorization: Bearer $CF_API_KEY"
```

## 接口列表

| 接口                                       | 方法 | 用途                                     |
| ------------------------------------------ | ---- | ---------------------------------------- |
| `/api/problems/detail`                     | GET  | 获取题单简介、画像和题目难度/标签摘要    |
| `/api/problems/update`                     | POST | 修改题库信息                             |
| `/api/problem/detail`                      | GET  | 获取单题中文题面 Markdown                |
| `/api/problems/chinese_list`               | GET  | 获取题单内所有题目的中文题面             |
| `/api/problem/admin_solution`              | GET  | 获取单题管理员题解                       |
| `/api/problem/list`                        | POST | 批量获取题目与管理员题解                 |
| `/api/problem/submit_proxy`                | POST | 代理登录 HydroOJ、提交代码并等待评测结果 |
| `/api/problem/upload_sol`                  | POST | 上传或更新管理员题解                     |
| `/api/problem/get_testdata`                | GET  | 获取题目测试数据                         |
| `/api/problem/upload_testdata`             | POST | 上传题目测试数据                         |
| `/api/problem/upload_zh_content`           | POST | 上传或更新题目中文题面                   |
| `/api/problem/create`                      | POST | 新建题目                                 |
| `/api/problem/update`                      | POST | 修改题目                                 |
| `/api/problem/generate_ai_alg_tag`         | POST | 生成并写入 AI 算法标签                   |
| `/api/problem-zip/export/problem/:pid`     | GET  | 导出单题 zip                             |
| `/api/problem-zip/export/pset/:psid`       | GET  | 流式下载题库 zip                         |
| `/api/problem-zip/export/pset/:psid/local` | POST | 启动题库本地打包任务                     |
| `/api/problem-zip/export/jobs`             | GET  | 列出本地导出任务                         |
| `/api/problem-zip/export/job/:jobId`       | GET  | 查询导出任务                             |
| `/api/problem-zip/export/job/:jobId`       | POST | 删除导出任务                             |
| `/api/problem-zip/export/job/:jobId/file`  | GET  | 下载导出 zip                             |
| `/api/problem-zip/export/job/:jobId/retry` | POST | 重试导出任务                             |
| `/api/problem-zip/import`                  | POST | 上传 zip 导入题目/题库                   |
| `/api/problem-zip/import/jobs`             | GET  | 列出导入任务                             |
| `/api/problem-zip/import/job/:jobId`       | GET  | 查询导入任务                             |
| `/api/problem-zip/import/job/:jobId`       | POST | 删除导入任务                             |
| `/api/problem-zip/import/job/:jobId/retry` | POST | 重试导入任务                             |

## GET `/api/problems/detail`

获取题单基础信息，以及每个章节下题目的难度和算法标签摘要。

### 请求参数

| 参数       | 必填 | 说明          |
| ---------- | ---- | ------------- |
| `domainId` | 是   | 域 ID         |
| `psid`     | 是   | 题单 ObjectId |

### 请求示例

```bash
curl "https://codefun2000.com/api/problems/detail?domainId=system&psid=65xxxxxxxxxxxxxxxxxxxxxx" \
  -H "X-Api-Key: $CF_API_KEY"
```

### 成功返回

```json
{
  "introduction": "题单介绍",
  "profile": "题单画像",
  "data": [
    {
      "title": "章节标题",
      "items": [
        {
          "id": 1,
          "diff": 3,
          "alg_tag": "动态规划"
        }
      ]
    }
  ]
}
```

## POST `/api/problems/update`

修改已有题库。只更新传入的字段。`psid` 可以是 MongoDB ObjectId，也可以是题库简称。更新 `dag` 时会同步题库-题目映射，并清缓存。

### 请求体

`Content-Type: application/json`

| 参数                              | 必填          | 说明                                                         |
| --------------------------------- | ------------- | ------------------------------------------------------------ |
| `domainId`                        | 改 DAG 时必填 | 域 ID，用于把章节里的题号解析成题目                          |
| `psid`                            | 是            | 题库 ObjectId 或简称                                         |
| `name`                            | 否            | 题库名称                                                     |
| `abbreviation`                    | 否            | 英文简称，不能与其它题库重复                                 |
| `company_tag`                     | 否            | 所属公司                                                     |
| `introduction`                    | 否            | 一句话简介                                                   |
| `profile`                         | 否            | 题库介绍                                                     |
| `usage`                           | 否            | 使用说明                                                     |
| `picture_url`                     | 否            | 封面图                                                       |
| `buying_guide`                    | 否            | 购买指南                                                     |
| `after_sales_guide`               | 否            | 售后指南                                                     |
| `purchase_url`                    | 否            | 外部购买链接                                                 |
| `price`                           | 否            | 价格                                                         |
| `origin_price` / `original_price` | 否            | 原价                                                         |
| `type`                            | 否            | `problem_set` / `course` / `codenote` / `training_camp`      |
| `dag`                             | 否            | 章节 JSON（编辑页同款：`_id`、`title`、`pids` 或训练营 `problems`） |
| `hidden`                          | 否            | 是否隐藏题库                                                 |
| `ownerOnly`                       | 否            | 是否仅拥有者可见                                             |
| `manual`                          | 否            | 是否手动授权（不走按价免费）                                 |
| `extra_pay`                       | 否            | 是否单独付费                                                 |
| `hidden_content`                  | 否            | 是否隐藏题面                                                 |
| `show_video`                      | 否            | 是否展示视频                                                 |
| `enableComment`                   | 否            | 是否展示评论区                                               |
| `useCodenoteTextSolRender`        | 否            | 题解是否用代码笔记样式                                       |
| `groupId`                         | 否            | 拼团 ID                                                      |
| `choicePracticeId`                | 否            | 关联选择题组                                                 |
| `enableChoicePractice`            | 否            | 为真时把选择题组设为本题库                                   |
| `pageConfig`                      | 否            | 前端页面配置，JSON 对象或字符串                              |
| `CodeNoteSetting`                 | 否            | 代码笔记配置，JSON 对象或字符串                              |
| `validDays`                       | 否            | 训练营有效天数                                               |
| `endTime`                         | 否            | 结束时间（datetime-local 或毫秒时间戳；空字符串清除）        |
| `top`                             | 否            | 列表排序，越小越靠前                                         |

### 请求示例

```bash
curl -X POST "https://codefun2000.com/api/problems/update" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: $CF_API_KEY" \
  -d '{
    "domainId": "system",
    "psid": "65xxxxxxxxxxxxxxxxxxxxxx",
    "name": "算法基础题库",
    "introduction": "从入门到进阶",
    "price": 99
  }'
```

更新章节（`pids` 用题号）：

```bash
curl -X POST "https://codefun2000.com/api/problems/update" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: $CF_API_KEY" \
  -d '{
    "domainId": "system",
    "psid": "algo-basic",
    "dag": [
      {
        "_id": 1,
        "title": "第一章",
        "requireNids": [],
        "pids": ["P1001", "P1002"]
      }
    ]
  }'
```

### 成功返回

```json
{
  "message": "problem set update success",
  "psid": "65xxxxxxxxxxxxxxxxxxxxxx",
  "name": "算法基础题库",
  "abbreviation": "algo-basic",
  "introduction": "从入门到进阶",
  "price": 99,
  "hidden": false,
  "type": "problem_set",
  "dagChapterCount": 1
}
```

传入 `dag` 时还会带回解析后的章节（题号形式）。

## GET `/api/problem/detail`

获取单个题目的中文题面 Markdown。

### 请求参数

| 参数       | 必填 | 说明     |
| ---------- | ---- | -------- |
| `domainId` | 是   | 域 ID    |
| `pid`      | 是   | 题目编号 |

### 请求示例

```bash
curl "https://codefun2000.com/api/problem/detail?domainId=system&pid=P1001" \
  -H "X-Api-Key: $CF_API_KEY"
```

### 成功返回

```json
{
  "data": "中文题面 Markdown 内容"
}
```

## GET `/api/problems/chinese_list`

获取指定题单内所有存在题目的中文题面。

### 请求参数

| 参数       | 必填 | 说明          |
| ---------- | ---- | ------------- |
| `domainId` | 是   | 域 ID         |
| `psid`     | 是   | 题单 ObjectId |

### 请求示例

```bash
curl "https://codefun2000.com/api/problems/chinese_list?domainId=system&psid=65xxxxxxxxxxxxxxxxxxxxxx" \
  -H "X-Api-Key: $CF_API_KEY"
```

### 成功返回

```json
{
  "data": [
    {
      "pid": "P1001",
      "content": "中文题面 Markdown 内容"
    }
  ]
}
```

## GET `/api/problem/admin_solution`

获取单题管理员题解。

### 请求参数

| 参数       | 必填 | 说明     |
| ---------- | ---- | -------- |
| `domainId` | 是   | 域 ID    |
| `pid`      | 是   | 题目编号 |

### 请求示例

```bash
curl "https://codefun2000.com/api/problem/admin_solution?domainId=system&pid=P1001" \
  -H "X-Api-Key: $CF_API_KEY"
```

### 成功返回

```json
{
  "data": [
    {
      "docId": "题解文档 ID",
      "content": "题解 Markdown 内容"
    }
  ]
}
```

## POST `/api/problem/list`

批量获取题目详情和管理员题解。

### 请求体

`Content-Type: application/json`

| 参数       | 必填 | 说明                                                       |
| ---------- | ---- | ---------------------------------------------------------- |
| `domainId` | 是   | 域 ID                                                      |
| `pids`     | 否   | 题目编号数组，例如 `["P1001", "P1002"]`                    |
| `query`    | 否   | HydroOJ 题目查询条件。`{"tag":"all"}` 表示扫描当前域内题目 |
| `latest`   | 否   | 配合 `query` 使用，按题号倒序截取最新 N 道                 |

`pids` 和 `query` 至少提供一个。使用 `query` 时会过滤隐藏题目和没有管理员题解的题目。

### 请求示例

```bash
curl -X POST "https://codefun2000.com/api/problem/list" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: $CF_API_KEY" \
  -d '{
    "domainId": "system",
    "pids": ["P1001", "P1002"]
  }'
```

按条件获取最新题目：

```bash
curl -X POST "https://codefun2000.com/api/problem/list" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: $CF_API_KEY" \
  -d '{
    "domainId": "system",
    "query": { "tag": "all" },
    "latest": 10
  }'
```

### 成功返回

```json
{
  "message": "",
  "data": [
    {
      "pid": "P1001",
      "title": "题目标题",
      "content": "中文题面 Markdown 内容",
      "psdocs": [
        {
          "content": "管理员题解 Markdown 内容"
        }
      ],
      "alg_tag": ["动态规划"],
      "re_type": "推荐分类"
    }
  ]
}
```

## POST `/api/problem/submit_proxy`

先校验站点秘钥，再代理登录 HydroOJ 后提交代码，并轮询等待评测完成。`uname`/`password` 只用于以该账号交题，不能替代秘钥。

### 请求体

`Content-Type: application/json`

| 参数             | 必填 | 默认值       | 说明                               |
| ---------------- | ---- | ------------ | ---------------------------------- |
| `domainId`       | 是   | -            | 域 ID，目前仅用于参数完整性校验    |
| `uname`          | 是   | -            | HydroOJ 交题账号                   |
| `password`       | 是   | -            | HydroOJ 交题密码                   |
| `pid`            | 是   | -            | 题目编号                           |
| `lang`           | 是   | -            | HydroOJ 语言标识                   |
| `code`           | 是   | -            | 源代码                             |
| `pretest`        | 否   | `false`      | 是否自测                           |
| `input`          | 否   | `""`         | 自测输入，仅 `pretest=true` 时使用 |
| `baseUrl`        | 否   | 当前请求站点 | HydroOJ 站点地址                   |
| `timeoutMs`      | 否   | `60000`      | 等待评测超时时间                   |
| `pollIntervalMs` | 否   | `1000`       | 轮询间隔                           |

### 请求示例

```bash
curl -X POST "https://codefun2000.com/api/problem/submit_proxy" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: $CF_API_KEY" \
  -d '{
    "domainId": "system",
    "uname": "'"$CF_UNAME"'",
    "password": "'"$CF_PASSWORD"'",
    "pid": "P1001",
    "lang": "cc.cc17",
    "code": "#include <bits/stdc++.h>\nusing namespace std;\nint main(){return 0;}"
  }'
```

### 成功返回

```json
{
  "ok": true,
  "rid": "评测记录 ID",
  "result": {
    "isAccepted": true,
    "status": {
      "code": 1,
      "name": "STATUS_ACCEPTED",
      "textZh": "完全通过"
    },
    "errorType": "无",
    "score": 100,
    "timeMs": 12,
    "memoryBytes": 1048576,
    "compilerMessage": "",
    "runtimeMessage": "",
    "firstFailedCase": null,
    "caseSummary": {
      "total": 10,
      "accepted": 10
    }
  }
}
```

超时时返回：

```json
{
  "ok": false,
  "rid": "评测记录 ID",
  "message": "提交已创建，但等待评测结果超时",
  "errorType": "超时"
}
```

## POST `/api/problem/upload_sol`

上传或更新单题管理员题解。

### 请求体

`Content-Type: application/json`

| 参数       | 必填 | 说明               |
| ---------- | ---- | ------------------ |
| `domainId` | 是   | 域 ID              |
| `pid`      | 是   | 题目编号           |
| `solution` | 是   | 题解 Markdown 内容 |

### 请求示例

```bash
curl -X POST "https://codefun2000.com/api/problem/upload_sol" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: $CF_API_KEY" \
  -d '{
    "domainId": "system",
    "pid": "P1001",
    "solution": "## 题解\n这里填写题解内容。"
  }'
```

### 成功返回

```text
P1001 solution upload success
```

## POST `/api/problem/upload_testdata`

上传题目测试数据。

### 请求体

`Content-Type: application/json`

| 参数        | 必填 | 默认值 | 说明                                           |
| ----------- | ---- | ------ | ---------------------------------------------- |
| `domainId`  | 是   | -      | 域 ID                                          |
| `pid`       | 是   | -      | 题目编号                                       |
| `files`     | 否   | -      | 文件名到文件内容的映射                         |
| `ioPairs`   | 否   | -      | 输入输出对数组，会转成 `{id}.in` 和 `{id}.out` |
| `overwrite` | 否   | `true` | 为 `false` 且已有测试数据时跳过上传            |

`files` 和 `ioPairs` 至少提供一个有效数据源。接口会以 UTF-8 文本写入测试数据文件。

### 请求示例：使用 `files`

```bash
curl -X POST "https://codefun2000.com/api/problem/upload_testdata" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: $CF_API_KEY" \
  -d '{
    "domainId": "system",
    "pid": "P1001",
    "files": {
      "1.in": "1 2\n",
      "1.out": "3\n"
    }
  }'
```

### 请求示例：使用 `ioPairs`

```bash
curl -X POST "https://codefun2000.com/api/problem/upload_testdata" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: $CF_API_KEY" \
  -d '{
    "domainId": "system",
    "pid": "P1001",
    "overwrite": false,
    "ioPairs": [
      {
        "id": "1",
        "input": "1 2\n",
        "output": "3\n"
      }
    ]
  }'
```

### 成功返回

```json
{
  "message": "testdata upload success",
  "pid": "P1001",
  "uploadedCount": 2,
  "uploadedFiles": ["1.in", "1.out"]
}
```

已有数据且 `overwrite=false` 时：

```json
{
  "message": "testdata already exists, skip upload (overwrite is false).",
  "pid": "P1001",
  "skipped": true,
  "existingTestdataCount": 10
}
```

## POST `/api/problem/upload_zh_content`

上传或更新题目的中文题面 Markdown。接口会写入题目 `content` JSON 中的 `zh` 字段，并保留已有其它语言字段。

### 请求体

`Content-Type: application/json`

| 参数       | 必填 | 说明                        |
| ---------- | ---- | --------------------------- |
| `domainId` | 是   | 域 ID                       |
| `pid`      | 是   | 题目编号                    |
| `content`  | 是   | 中文题面 Markdown，不能为空 |

### 请求示例

```bash
curl -X POST "https://codefun2000.com/api/problem/upload_zh_content" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: $CF_API_KEY" \
  -d '{
    "domainId": "system",
    "pid": "P1001",
    "content": "# 题目标题\n\n题目描述..."
  }'
```

### 成功返回

```json
{
  "message": "zh problem content upload success",
  "pid": "P1001"
}
```

## GET `/api/problem/get_testdata`

获取题目测试数据（UTF-8 文本）。同时返回文件名映射和成对的 `ioPairs`。

### 请求参数

| 参数       | 必填 | 说明     |
| ---------- | ---- | -------- |
| `domainId` | 是   | 域 ID    |
| `pid`      | 是   | 题目编号 |

### 请求示例

```bash
curl "https://codefun2000.com/api/problem/get_testdata?domainId=system&pid=P1001" \
  -H "X-Api-Key: $CF_API_KEY"
```

### 成功返回

```json
{
  "pid": "P1001",
  "fileCount": 2,
  "files": {
    "1.in": "1 2\n",
    "1.out": "3\n"
  },
  "ioPairs": [
    {
      "id": "1",
      "input": "1 2\n",
      "output": "3\n"
    }
  ]
}
```

## POST `/api/problem/create`

新建题目。写操作用站点管理员身份（`ADMIN_UID`）。

### 请求体

`Content-Type: application/json`

| 参数             | 必填 | 说明                             |
| ---------------- | ---- | -------------------------------- |
| `domainId`       | 是   | 域 ID                            |
| `pid`            | 是   | 题目编号                         |
| `content`        | 是   | 中文题面 Markdown                |
| `title`          | 否   | 题目标题，缺省为 `pid`           |
| `hidden`         | 否   | 是否隐藏，默认 `false`           |
| `difficulty`     | 否   | 难度，默认 `0`                   |
| `tag` / `tags`   | 否   | Hydro 标签，逗号分隔字符串或数组 |
| `alg_tag`        | 否   | 算法标签                         |
| `ai_alg_tags`    | 否   | AI 算法标签                      |
| `videosol`       | 否   | 视频题解                         |
| `trial_videosol` | 否   | 试看视频题解                     |

### 请求示例

```bash
curl -X POST "https://codefun2000.com/api/problem/create" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: $CF_API_KEY" \
  -d '{
    "domainId": "system",
    "pid": "P1001",
    "title": "A + B Problem",
    "content": "# A + B\n\n输入两个整数，输出它们的和。"
  }'
```

## POST `/api/problem/update`

修改已有题目。只更新传入的字段。

### 请求体

`Content-Type: application/json`

| 参数             | 必填 | 说明              |
| ---------------- | ---- | ----------------- |
| `domainId`       | 是   | 域 ID             |
| `pid`            | 是   | 当前题目编号      |
| `newPid`         | 否   | 新题目编号        |
| `title`          | 否   | 题目标题          |
| `content`        | 否   | 中文题面 Markdown |
| `hidden`         | 否   | 是否隐藏          |
| `difficulty`     | 否   | 难度              |
| `tag` / `tags`   | 否   | Hydro 标签        |
| `alg_tag`        | 否   | 算法标签          |
| `ai_alg_tags`    | 否   | AI 算法标签       |
| `videosol`       | 否   | 视频题解          |
| `trial_videosol` | 否   | 试看视频题解      |

### 请求示例

```bash
curl -X POST "https://codefun2000.com/api/problem/update" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: $CF_API_KEY" \
  -d '{
    "domainId": "system",
    "pid": "P1001",
    "title": "A + B Problem（修订）",
    "difficulty": 1
  }'
```

## POST `/api/problem/generate_ai_alg_tag`

调用编辑页同款逻辑生成 AI 算法标签，并写入 `problem_info.extra.ai_alg_tags`。

### 请求体

`Content-Type: application/json`

| 参数       | 必填 | 默认值  | 说明                     |
| ---------- | ---- | ------- | ------------------------ |
| `domainId` | 是   | -       | 域 ID                    |
| `pid`      | 是   | -       | 题目编号                 |
| `cover`    | 否   | `false` | 为 `true` 时覆盖已有标签 |

### 请求示例

```bash
curl -X POST "https://codefun2000.com/api/problem/generate_ai_alg_tag" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: $CF_API_KEY" \
  -d '{
    "domainId": "system",
    "pid": "P1001",
    "cover": false
  }'
```

## 题目压缩包 `/api/problem-zip/*`

导入导出 zip 与控制面板「题目压缩包」页使用同一组接口。外部调用带秘钥；管理员在页面上用登录态即可。

删除任务可用 `POST` 或 `DELETE`。本地打包支持 `Range` 断点下载。

## GET `/api/problem-zip/export/problem/:pid`

打包并下载单题 zip。

```bash
curl -OJ "https://codefun2000.com/api/problem-zip/export/problem/P1001" \
  -H "X-Api-Key: $CF_API_KEY"
```

## GET `/api/problem-zip/export/pset/:psid`

流式下载整个题库 zip（可能较长时间占用连接）。大题库更建议走本地打包任务。

```bash
curl -OJ "https://codefun2000.com/api/problem-zip/export/pset/65xxxxxxxxxxxxxxxxxxxxxx" \
  -H "X-Api-Key: $CF_API_KEY"
```

## POST `/api/problem-zip/export/pset/:psid/local`

在服务器上启动题库打包任务，完成后用 file 接口下载。

```bash
curl -X POST "https://codefun2000.com/api/problem-zip/export/pset/65xxxxxxxxxxxxxxxxxxxxxx/local" \
  -H "X-Api-Key: $CF_API_KEY"
```

成功时返回 `{ "ok": true, "job": { "jobId", "status", "done", "total", ... }, "reused": false }`。已有进行中的任务时返回 `error` 与 `runningJob`。

## GET `/api/problem-zip/export/jobs`

列出本地导出任务。

```bash
curl "https://codefun2000.com/api/problem-zip/export/jobs" \
  -H "X-Api-Key: $CF_API_KEY"
```

## GET `/api/problem-zip/export/job/:jobId`

查询单个导出任务。`status` 为 `done` 时 `downloadUrl` 可用。

```bash
curl "https://codefun2000.com/api/problem-zip/export/job/$JOB_ID" \
  -H "X-Api-Key: $CF_API_KEY"
```

## GET `/api/problem-zip/export/job/:jobId/file`

下载已完成的导出 zip，支持 `Range`。

```bash
curl -OJ "https://codefun2000.com/api/problem-zip/export/job/$JOB_ID/file" \
  -H "X-Api-Key: $CF_API_KEY"
```

未完成时返回 JSON：`{ "error": "尚未打包完成", "job": { ... } }`。

## POST `/api/problem-zip/export/job/:jobId/retry`

重试失败的导出任务。

```bash
curl -X POST "https://codefun2000.com/api/problem-zip/export/job/$JOB_ID/retry" \
  -H "X-Api-Key: $CF_API_KEY"
```

## POST `/api/problem-zip/export/job/:jobId`

删除导出任务及生成的文件。

```bash
curl -X POST "https://codefun2000.com/api/problem-zip/export/job/$JOB_ID" \
  -H "X-Api-Key: $CF_API_KEY"
```

## POST `/api/problem-zip/import`

上传 zip，导入单题或题库。`multipart/form-data`，文件字段名为 `file`。

| 字段           | 必填 | 说明                   |
| -------------- | ---- | ---------------------- |
| `file`         | 是   | zip 文件               |
| `pid`          | 否   | 导入为单题时指定题号   |
| `psid`         | 否   | 导入到已有题库         |
| `name`         | 否   | 新建题库名称           |
| `abbreviation` | 否   | 新建题库简称           |
| `overwrite`    | 否   | 为真时覆盖已有题目数据 |

```bash
curl -X POST "https://codefun2000.com/api/problem-zip/import" \
  -H "X-Api-Key: $CF_API_KEY" \
  -F "file=@/path/to/P1001.zip" \
  -F "pid=P1001" \
  -F "overwrite=1"
```

成功返回 `{ "ok": true, "job": { "jobId", "status", ... }, "reused": false }`。用下面的 jobs 接口轮询直到 `status` 为 `done` 或 `error`。

## GET `/api/problem-zip/import/jobs`

列出导入任务。

```bash
curl "https://codefun2000.com/api/problem-zip/import/jobs" \
  -H "X-Api-Key: $CF_API_KEY"
```

## GET `/api/problem-zip/import/job/:jobId`

查询单个导入任务。

```bash
curl "https://codefun2000.com/api/problem-zip/import/job/$JOB_ID" \
  -H "X-Api-Key: $CF_API_KEY"
```

## POST `/api/problem-zip/import/job/:jobId/retry`

重试失败的导入任务。

```bash
curl -X POST "https://codefun2000.com/api/problem-zip/import/job/$JOB_ID/retry" \
  -H "X-Api-Key: $CF_API_KEY"
```

## POST `/api/problem-zip/import/job/:jobId`

删除导入任务。

```bash
curl -X POST "https://codefun2000.com/api/problem-zip/import/job/$JOB_ID" \
  -H "X-Api-Key: $CF_API_KEY"
```

## 调用建议

1. 在服务端保存站点秘钥，通过环境变量传入，例如 `CF_API_KEY`。不要写入公开仓库或前端页面。
2. 秘钥在 `/manage/external-api` 查看与轮换；默认约 24 小时过期，刷新后旧钥立刻作废。
3. 上传类接口会修改题目数据，调用前建议先在测试域验证。
4. `submit_proxy` 会等待评测结果，外部调用方应设置自己的 HTTP 超时大于 `timeoutMs`；交题账号用 `CF_UNAME` / `CF_PASSWORD`，与秘钥分开保存。
5. 测试数据上传目前按 UTF-8 文本处理，不适合直接上传二进制文件。
6. 批量查询接口可能触发多次数据库读取，建议控制 `pids` 数量或分批调用。
7. 大题库导出请用 `/api/problem-zip/export/pset/:psid/local` 后台打包，再下载 file；不要长时间占用流式接口。
8. 压缩包接口的域取自当前 Hydro 域；需要指定域时使用 `/d/<domainId>/api/problem-zip/...`。