"""
OJ 题目重写与上传自动化脚本

流程：
  Step 1: 获取原始题面
  Step 2: 获取题解代码
  Step 3: 生成新题面（默认由 Cursor Agent 写入 JSON；可选 DeepSeek）
  Step 3.5: 生成模板题解
  Step 4: 生成新样例
  Step 5: 脚本拼接完整题面
  Step 6: 上传原始题面为附加文件
  Step 7: 上传新题面和新标题
  Step 8: 上传题解

调试模式：
  --mode 0: 完整流程（默认）
  --mode 1: 交互暂停模式
  --mode 2: 仅获取数据
  --mode 3: 仅拼接（Agent 源读取已有产物；DeepSeek 源会先调用 LLM）
  --mode 4: 仅上传数据（需已有 05 拼接题面）
  --mode 5: 仅重新生成模板题解并上传
  --mode 6: 读取 Agent 产物（03/03.5/04），拼接并上传

--source agent（默认）：不调用 DeepSeek，读取 log/{pid}/ 中 Agent 写入的文件
--source deepseek：原 LLM 流程，需要 DEEPSEEK_API_KEY

环境变量：HYDRO_API_UNAME, HYDRO_API_PASSWORD；（仅 deepseek）DEEPSEEK_API_KEY
"""
from __future__ import annotations

import argparse

import argparse
import json
import os
import re
import shutil
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path

import requests
from openai import OpenAI

# ============================================================
# 全局配置
# ============================================================
BASE_URL = "https://codefun2000.com"
DOMAIN_ID = "system"
MAX_RETRIES = 3          # LLM 调用失败最大重试次数
LLM_MODEL = "deepseek-v4-pro"
LLM_BASE_URL = "https://api.deepseek.com"
RETRY_DELAY_SEC = 2      # 重试间隔（秒）

# 退出码
EXIT_SUCCESS = 0               # 成功
EXIT_ALREADY_DONE = 0          # 已成功处理过，跳过
EXIT_STEP1_FAILED = 11         # Step 1 失败
EXIT_STEP2_FAILED = 12         # Step 2 失败
EXIT_STEP3_FAILED = 13         # Step 3 失败
EXIT_STEP35_FAILED = 14        # Step 3.5 失败
EXIT_STEP4_FAILED = 15         # Step 4 失败
EXIT_STEP5_FAILED = 16         # Step 5 失败
EXIT_STEP6_FAILED = 17         # Step 6 失败
EXIT_STEP7_FAILED = 18         # Step 7 失败
EXIT_STEP8_FAILED = 19         # Step 8 失败
EXIT_ENV_ERROR = 20            # 环境变量缺失
EXIT_MISSING_FILE = 21         # 模式 4/6 缺少必要文件
EXIT_WAITING_AGENT = 22        # Agent 产物未写齐，等待人工/Agent 补全

FILE_PROBLEM_JSON = "03_LLM生成的新题面.json"
FILE_SOLUTION_MD = "03.5_修改后的题解.md"
FILE_SAMPLES_JSON = "04_LLM生成的新样例.json"
FILE_ASSEMBLED_MD = "05_拼接后的完整题面.md"
KEEP_LOG_MODES = {4, 5, 6}

# ============================================================
# 工具函数
# ============================================================

def get_script_dir() -> Path:
    return Path(__file__).resolve().parent


def get_log_dir(pid: str) -> Path:
    return get_script_dir() / "log" / pid


def init_logger(log_dir: Path):
    """初始化日志文件，返回日志写入函数"""
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "执行日志.txt"

    def log(msg: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] {msg}"
        print(line)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    # 写入启动分隔线
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"执行开始: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'='*60}\n")
    return log


def check_env_vars(log, source: str = "agent") -> bool:
    """检查必需的环境变量。agent 源不需要 DeepSeek。"""
    required = ["HYDRO_API_UNAME", "HYDRO_API_PASSWORD"]
    if source == "deepseek":
        required.append("DEEPSEEK_API_KEY")
    missing = [var for var in required if not (os.environ.get(var) or "").strip()]
    if missing:
        log(f"错误：缺少环境变量: {', '.join(missing)}")
        log("请设置后再运行：")
        log('  $env:HYDRO_API_UNAME="luti"')
        log('  $env:HYDRO_API_PASSWORD="your-password"')
        if source == "deepseek":
            log('  $env:DEEPSEEK_API_KEY="your-deepseek-api-key"')
        return False
    return True


def require_https(url: str):
    if not url.startswith("https://"):
        raise ValueError("出于通信安全考虑，BASE_URL 必须是 https:// 开头")


def save_text(path: Path, content: str, log):
    """保存文本到文件"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    log(f"  已保存: {path}")


def save_json(path: Path, data, log):
    """保存 JSON 到文件"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2))
    log(f"  已保存: {path}")


def pause_if_mode1(mode: int, msg: str):
    """模式 1 下暂停等待用户确认"""
    if mode == 1:
        print(f"\n{'='*40}")
        print(f"[暂停] {msg}")
        input("按回车键继续...")


# ============================================================
# Step 1: 获取原始题面
# ============================================================

def step1_fetch_problem(pid: str, log, log_dir: Path) -> tuple[str, str] | None:
    """
    调用 GET /api/problem/detail 获取原始题面，
    调用 POST /api/problem/list 获取标题。
    返回 (markdown_text, title)，失败返回 None
    """
    log(f"\n{'─'*40}")
    log(f"Step 1: 获取原始题面 (PID={pid})")

    uname = os.environ["HYDRO_API_UNAME"]
    password = os.environ["HYDRO_API_PASSWORD"]

    # --- 1a. 获取题面 ---
    params = {
        "domainId": DOMAIN_ID,
        "uname": uname,
        "password": password,
        "pid": pid,
    }

    url = f"{BASE_URL}/api/problem/detail"
    try:
        resp = requests.get(url, params=params, timeout=(5, 20), verify=True)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        log(f"错误：请求题面接口失败：{e}")
        return None

    try:
        data = resp.json()
    except ValueError:
        log(f"错误：接口返回非 JSON，HTTP {resp.status_code}，响应片段：{resp.text[:200]!r}")
        return None

    if not isinstance(data, dict) or "data" not in data:
        log(f"错误：接口返回格式异常：{json.dumps(data, ensure_ascii=False)[:300]}")
        return None

    markdown_text = data.get("data", "")
    if not isinstance(markdown_text, str) or not markdown_text.strip():
        log("错误：题面内容为空")
        return None

    log(f"成功获取题面，长度：{len(markdown_text)} 字符")
    save_text(log_dir / "01_原始题面.md", markdown_text, log)

    # --- 1b. 获取标题 ---
    list_payload = {
        "domainId": DOMAIN_ID,
        "uname": uname,
        "password": password,
        "pids": [pid],
    }

    list_url = f"{BASE_URL}/api/problem/list"
    try:
        list_resp = requests.post(
            list_url,
            json=list_payload,
            timeout=(5, 20),
            verify=True,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        list_resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        log(f"错误：请求题目列表接口失败：{e}")
        return None

    try:
        list_data = list_resp.json()
    except ValueError:
        log(f"错误：列表接口返回非 JSON，响应片段：{list_resp.text[:200]!r}")
        return None

    if not isinstance(list_data, dict) or "data" not in list_data:
        log(f"错误：列表接口返回格式异常")
        return None

    pdocs = list_data.get("data", [])
    if not isinstance(pdocs, list) or len(pdocs) == 0:
        log("错误：列表接口未返回题目数据")
        return None

    title = pdocs[0].get("title", "")
    if not title:
        log("警告：未能从 API 获取标题，使用 pid 作为标题")
        title = pid

    log(f"原始标题: {title}")
    save_text(log_dir / "01_原始标题.txt", title, log)
    return (markdown_text, title)


# ============================================================
# Step 2: 获取题解代码
# ============================================================

def _is_valid_code(code: str) -> bool:
    """检查提取的代码块是否像是真实代码（非纯标签/语言名）"""
    stripped = code.strip()
    if len(stripped) < 10:
        return False
    if re.fullmatch(r'[a-zA-Z0-9\s]+', stripped):
        return False
    return True


def extract_code_block(solution_text: str) -> str | None:
    """从题解文本中提取第一个有效的 ```...``` 代码块。跳过纯字母数字或过短的块。"""
    pattern = r'```[^\S\n]*\n(.*?)```'
    for match in re.finditer(pattern, solution_text, re.DOTALL):
        code = match.group(1).strip()
        if _is_valid_code(code):
            return code
    return None


def step2_fetch_solution(pid: str, log, log_dir: Path) -> tuple[str, str] | None:
    """
    调用 GET /api/problem/admin_solution 获取管理员题解
    提取第一个有效代码块和完整题解文本
    返回 (code, full_solution_markdown)，失败返回 None
    """
    log(f"\n{'─'*40}")
    log(f"Step 2: 获取题解代码 (PID={pid})")

    uname = os.environ["HYDRO_API_UNAME"]
    password = os.environ["HYDRO_API_PASSWORD"]

    params = {
        "domainId": DOMAIN_ID,
        "uname": uname,
        "password": password,
        "pid": pid,
    }

    url = f"{BASE_URL}/api/problem/admin_solution"
    try:
        resp = requests.get(url, params=params, timeout=(5, 20), verify=True)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        log(f"错误：请求题解接口失败：{e}")
        return None

    try:
        data = resp.json()
    except ValueError:
        log(f"错误：接口返回非 JSON，HTTP {resp.status_code}，响应片段：{resp.text[:200]!r}")
        return None

    if not isinstance(data, dict):
        log(f"错误：接口返回格式异常：{data!r}")
        return None

    if "data" not in data or not isinstance(data["data"], list) or len(data["data"]) == 0:
        log("错误：该题目没有管理员题解")
        return None

    psdocs = data["data"]
    log(f"获取到 {len(psdocs)} 篇管理员题解")

    # 遍历所有题解，找到第一个包含有效代码块的
    for i, psdoc in enumerate(psdocs):
        content = psdoc.get("content", "")
        if isinstance(content, str):
            code = extract_code_block(content)
            if code:
                log(f"在第 {i+1} 篇题解中找到有效代码块，长度：{len(code)} 字符")
                save_text(log_dir / "02_题解代码.py", code, log)
                save_text(log_dir / "02_原始完整题解.md", content, log)
                return (code, content)

    # 没找到有效代码块，回退：将整篇题解作为代码
    log("警告：未找到有效代码块，将使用完整题解文本作为代码")
    for i, psdoc in enumerate(psdocs):
        content = psdoc.get("content", "")
        if isinstance(content, str) and content.strip():
            log(f"使用第 {i+1} 篇题解全文，长度：{len(content)} 字符")
            save_text(log_dir / "02_题解代码.py", content, log)
            save_text(log_dir / "02_原始完整题解.md", content, log)
            return (content, content)

    log("错误：所有题解均为空")
    return None


# ============================================================
# LLM 调用封装
# ============================================================

def create_llm_client(log) -> OpenAI | None:
    """创建 LLM 客户端"""
    api_key = (os.environ.get("DEEPSEEK_API_KEY") or "").strip()
    if not api_key:
        log("错误：未设置 DEEPSEEK_API_KEY 环境变量")
        return None
    return OpenAI(api_key=api_key, base_url=LLM_BASE_URL)


def call_llm(
    client: OpenAI,
    system_prompt: str,
    user_prompt: str,
    log,
) -> tuple[str, str] | None:
    """
    调用 LLM，开启思考模式（thinking）。
    返回 (content, reasoning_content)，失败返回 None。
    """
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            stream=False,
            reasoning_effort="high",
            extra_body={"thinking": {"type": "enabled"}},
        )
        message = response.choices[0].message
        # 思考模式下，reasoning_content 包含思考过程，content 包含最终答案
        reasoning = getattr(message, "reasoning_content", "") or ""
        content = message.content
        if reasoning:
            log(f"  LLM 思考过程长度: {len(reasoning)} 字符")
        if content is None:
            log("LLM 返回空 content（可能全部在 reasoning_content 中）")
            return None
        return (content, reasoning)
    except Exception as e:
        log(f"LLM 调用异常：{e}")
        return None


def save_llm_conversation(
    log_dir: Path,
    step_prefix: str,
    system_prompt: str,
    user_prompt: str,
    content: str | None,
    reasoning: str,
    attempt: int,
):
    """保存 LLM 对话记录到 log 目录"""
    conv_dir = log_dir / "llm_conversations"
    conv_dir.mkdir(parents=True, exist_ok=True)
    conv_path = conv_dir / f"{step_prefix}_attempt{attempt}.json"
    conv = {
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "response": content,
        "reasoning_content": reasoning,
    }
    with open(conv_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(conv, ensure_ascii=False, indent=2))


def call_llm_with_retry(
    client: OpenAI,
    system_prompt: str,
    user_prompt: str,
    log,
    step_name: str,
    log_dir: Path | None = None,
    step_prefix: str = "",
    validator: callable = None,
) -> str | None:
    """
    带重试的 LLM 调用。
    返回 content 文本，超过 MAX_RETRIES 次失败后返回 None。
    若提供 log_dir，每次尝试的对话会保存到 llm_conversations/ 子目录。
    若提供 validator，会对返回的 content 调用 validator(content)，返回 False 时触发重试。
    """
    for attempt in range(1, MAX_RETRIES + 1):
        log(f"  LLM 调用 (第 {attempt}/{MAX_RETRIES} 次)...")
        llm_result = call_llm(client, system_prompt, user_prompt, log)
        if llm_result is not None:
            content, reasoning = llm_result
        else:
            content, reasoning = None, ""
        if log_dir is not None and step_prefix:
            save_llm_conversation(log_dir, step_prefix, system_prompt, user_prompt, content, reasoning, attempt)
        if content is not None:
            if validator is not None:
                if not validator(content):
                    log(f"  结果验证失败，将重试")
                    if attempt < MAX_RETRIES:
                        time.sleep(RETRY_DELAY_SEC)
                    continue
            log(f"  LLM 调用成功")
            return content
        if attempt < MAX_RETRIES:
            log(f"  重试中，等待 {RETRY_DELAY_SEC} 秒...")
            time.sleep(RETRY_DELAY_SEC)
    log(f"错误：{step_name} 失败，已达最大重试次数 ({MAX_RETRIES})")
    return None


def extract_json_from_llm_response(response: str, log) -> dict | None:
    """
    从 LLM 响应中提取 JSON。
    支持响应中包含 ```json ... ``` 代码块或直接 JSON。
    """
    # 尝试提取 ```json ... ``` 代码块
    json_block_pattern = r'```json\s*\n(.*?)```'
    match = re.search(json_block_pattern, response, re.DOTALL)
    if match:
        json_str = match.group(1).strip()
    else:
        # 尝试提取 ``` ... ``` 代码块
        code_block_pattern = r'```\s*\n(.*?)```'
        match = re.search(code_block_pattern, response, re.DOTALL)
        if match:
            json_str = match.group(1).strip()
        else:
            # 直接尝试解析整个响应
            json_str = response.strip()

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        log(f"JSON 解析失败：{e}")
        log(f"尝试解析的文本前 500 字符：{json_str[:500]}")
        return None


def normalize_problem_data(result: dict) -> dict:
    """修正 LaTeX 双重转义。"""
    for field in ["content", "input_description", "output_description"]:
        if field in result and isinstance(result[field], str):
            result[field] = result[field].replace("\\\\", "\\")
    return result


def load_problem_json(log_dir: Path, log) -> dict | None:
    """从 Agent/LLM 产物读取新题面 JSON。"""
    path = log_dir / FILE_PROBLEM_JSON
    if not path.exists():
        log(f"缺少 Agent 产物: {path.name}")
        return None
    try:
        result = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        log(f"错误：读取 {path.name} 失败：{e}")
        return None
    if not isinstance(result, dict):
        log(f"错误：{path.name} 不是 JSON 对象")
        return None
    for field in ["title", "content", "input_description", "output_description"]:
        if field not in result or not str(result.get(field, "")).strip():
            log(f"错误：{path.name} 缺少字段 {field}")
            return None
    result = normalize_problem_data(result)
    log(f"已读取 Agent 题面: {result['title']}")
    return result


def validate_solution_markdown(text: str, log) -> bool:
    stripped = (text or "").strip()
    if not stripped:
        log("  验证失败：题解为空")
        return False
    for heading in ["## 解题思路", "## 复杂度分析", "## 代码实现"]:
        if heading not in stripped:
            log(f"  验证失败：缺少 {heading}")
            return False
    if "### Python" not in stripped or "### Java" not in stripped or "### C++" not in stripped:
        log("  验证失败：缺少 Python/Java/C++ 三语言小节")
        return False
    return True


def load_solution_markdown(log_dir: Path, log) -> str | None:
    path = log_dir / FILE_SOLUTION_MD
    if not path.exists():
        log(f"缺少 Agent 产物: {path.name}")
        return None
    text = path.read_text(encoding="utf-8").strip()
    if not validate_solution_markdown(text, log):
        return None
    log(f"已读取 Agent 题解，长度：{len(text)} 字符")
    return text


def load_samples_json(log_dir: Path, log) -> list | None:
    path = log_dir / FILE_SAMPLES_JSON
    if not path.exists():
        log(f"缺少 Agent 产物: {path.name}")
        return None
    try:
        result = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        log(f"错误：读取 {path.name} 失败：{e}")
        return None
    samples = result.get("samples") if isinstance(result, dict) else None
    if not isinstance(samples, list) or not samples:
        log(f"错误：{path.name} 缺少 samples 或为空")
        return None
    for i, sample in enumerate(samples, 1):
        if not isinstance(sample, dict) or not all(k in sample for k in ("input", "output", "explanation")):
            log(f"错误：样例 {i} 缺少 input/output/explanation")
            return None

    orig_path = log_dir / "01_原始题面.md"
    if orig_path.exists():
        from forbid_orig_sample import original_forbidden, sample_hits_original

        forbidden = original_forbidden(orig_path.read_text(encoding="utf-8"))
        for i, sample in enumerate(samples, 1):
            hit = sample_hits_original(sample.get("input", ""), forbidden)
            if hit:
                log(
                    f"错误：样例 {i} 仍使用原题面样例（{hit}）。"
                    "必须全部换成全新输入，特征行（含字母/问号的行、至少 3 个数的数据行）也不得复用。"
                )
                return None
    log(f"已读取 Agent 样例 {len(samples)} 条")
    return samples


def missing_agent_artifacts(log_dir: Path) -> list[str]:
    needed = [FILE_PROBLEM_JSON, FILE_SOLUTION_MD, FILE_SAMPLES_JSON]
    return [name for name in needed if not (log_dir / name).exists()]


def apply_title_prefix(title: str, original_title: str, log) -> str:
    prefix_match = re.match(r"^(第\d+题-)", original_title or "")
    if prefix_match:
        prefix = prefix_match.group(1)
        if not title.startswith(prefix):
            title = f"{prefix}{title}"
        log(f"原始标题前缀: {prefix}")
        log(f"最终标题: {title}")
    return title


# ============================================================
# 提示词加载
# ============================================================

PROMPTS_DIR = get_script_dir() / "prompts"


def load_prompt(filename: str) -> str:
    """从 prompts/ 目录加载提示词文件"""
    path = PROMPTS_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"提示词文件不存在: {path}")
    return path.read_text(encoding="utf-8")


# ============================================================
# Step 3: LLM 生成新题面
# ============================================================

STEP3_SYSTEM_PROMPT = load_prompt("step3_system.txt")


def step3_generate_problem_statement(
    original_statement: str,
    solution_code: str,
    log,
    log_dir: Path,
    source: str = "agent",
) -> dict | None:
    """
    生成新题面（标题 + 内容 + 输入输出描述，不含样例）。
    source=agent 时读取 log 中已有 JSON；source=deepseek 时调用 LLM。
    """
    log(f"\n{'─'*40}")
    log(f"Step 3: 生成新题面 (source={source})")
    if source == "agent":
        return load_problem_json(log_dir, log)

    client = create_llm_client(log)
    if client is None:
        return None

    step3_user_template = load_prompt("step3_user.txt")
    user_prompt = step3_user_template.format(
        original_statement=original_statement,
        solution_code=solution_code,
    )

    # 验证器：检查 JSON 合法性及必要字段
    def validate_step3(response_text: str) -> bool:
        result = extract_json_from_llm_response(response_text, log)
        if result is None:
            return False
        for field in ["title", "content", "input_description", "output_description"]:
            if field not in result:
                log(f"  验证失败：缺少字段 {field}")
                return False
        return True

    response = call_llm_with_retry(
        client, STEP3_SYSTEM_PROMPT, user_prompt, log, "生成新题面",
        log_dir=log_dir, step_prefix="step3",
        validator=validate_step3,
    )
    if response is None:
        return None

    # 保存原始响应
    save_text(log_dir / "03_LLM生成的新题面_原始响应.txt", response, log)

    # 解析 JSON（validator 已保证可解析）
    result = extract_json_from_llm_response(response, log)

    # 验证必要字段（validator 已保证，此处仅为安全兜底）
    required_fields = ["title", "content", "input_description", "output_description"]
    for field in required_fields:
        if field not in result:
            log(f"错误：LLM 返回的 JSON 缺少字段: {field}")
            return None

    # 修正 LaTeX 转义：LLM 可能对 JSON 中的反斜杠做了双重转义
    # 导致 json.loads 后出现 \\le 而不是 \le
    for field in ["content", "input_description", "output_description"]:
        result[field] = result[field].replace("\\\\", "\\")

    log(f"新标题: {result['title']}")
    log(f"新题面内容长度: {len(result['content'])} 字符")
    save_json(log_dir / "03_LLM生成的新题面.json", result, log)
    return result


# ============================================================
# Step 3.5: 检查题解是否需要修改
# ============================================================

STEP35_SYSTEM_PROMPT = load_prompt("step35_system.txt")


def step35_check_and_fix_solution(
    problem_data: dict,
    full_solution_md: str,
    log,
    log_dir: Path,
    source: str = "agent",
) -> tuple[str | None, bool]:
    """
    检查新题面与原题解是否有冲突（如题解中提到了新题面不存在的概念）。
    如果需要修改，LLM 生成适配新题面的题解。
    返回 (new_solution_or_None, success):
      - (new_solution, True): 题解需要修改，new_solution 为修改后的题解
      - (None, True): 题解无需修改
      - (None, False): LLM 调用失败
    """
    log(f"\n{'─'*40}")
    log(f"Step 3.5: 生成模板题解 (source={source})")
    if source == "agent":
        new_solution = load_solution_markdown(log_dir, log)
        if new_solution is None:
            return (None, False)
        return (new_solution, True)

    client = create_llm_client(log)
    if client is None:
        return (None, False)

    # 构造新题面描述
    new_problem_desc = f"""# {problem_data['title']}

# 题目内容
{problem_data['content']}

# 输入描述
{problem_data['input_description']}

# 输出描述
{problem_data['output_description']}"""

    step35_user_template = load_prompt("step35_user.txt")
    user_prompt = step35_user_template.format(
        new_problem_desc=new_problem_desc,
        full_solution_md=full_solution_md,
    )

    # 验证器：检查 LLM 返回是否为合法模板题解（含三语言代码块）
    def validate_response(response_text: str) -> bool:
        stripped = response_text.strip()
        if not stripped:
            log("  验证失败：响应为空")
            return False
        # 必须包含三个章节标题
        if "## 解题思路" not in stripped:
            log("  验证失败：缺少 ## 解题思路")
            return False
        if "## 复杂度分析" not in stripped:
            log("  验证失败：缺少 ## 复杂度分析")
            return False
        if "## 代码实现" not in stripped:
            log("  验证失败：缺少 ## 代码实现")
            return False
        # 必须包含三语言代码块
        if "### Python" not in stripped or "### Java" not in stripped or "### C++" not in stripped:
            log("  验证失败：缺少 Python/Java/C++ 三语言小节")
            return False
        return True

    response = call_llm_with_retry(
        client, STEP35_SYSTEM_PROMPT, user_prompt, log, "生成模板题解",
        log_dir=log_dir, step_prefix="step35",
        validator=validate_response,
    )
    if response is None:
        log("错误：Step 3.5 失败，已达最大重试次数")
        return (None, False)

    # 保存原始响应
    save_text(log_dir / "03.5_LLM题解检查_原始响应.txt", response, log)

    # 直接使用整个响应作为题解（纯 Markdown，不包裹 JSON）
    new_solution = response.strip()
    # 若响应被 ```json 或 ``` 代码块包裹，剥离外层代码块标记
    if new_solution.startswith("```"):
        lines = new_solution.splitlines()
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        new_solution = "\n".join(lines).strip()
    log(f"生成模板题解，长度：{len(new_solution)} 字符")
    save_text(log_dir / "03.5_修改后的题解.md", new_solution, log)
    save_json(log_dir / "03.5_题解检查结果.json", {"new_solution": new_solution}, log)
    return (new_solution, True)


# ============================================================
# Step 8: 上传题解
# ============================================================

def step8a_upload_original_solution(
    pid: str,
    original_solution: str,
    log,
    log_dir: Path,
) -> bool:
    """
    调用 POST /api/problem/upload_testdata 上传原始题解为附加文件
    """
    log(f"\n{'─'*40}")
    log("Step 8a: 上传原始题解文件")

    uname = os.environ["HYDRO_API_UNAME"]
    password = os.environ["HYDRO_API_PASSWORD"]

    payload = {
        "domainId": DOMAIN_ID,
        "uname": uname,
        "password": password,
        "pid": pid,
        "files": {
            "original_solution.md": original_solution,
        },
        "overwrite": True,
    }

    url = f"{BASE_URL}/api/problem/upload_testdata"
    try:
        resp = requests.post(
            url,
            json=payload,
            timeout=(10, 60),
            verify=True,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
    except requests.exceptions.RequestException as e:
        log(f"错误：上传原始题解请求失败：{e}")
        return False

    log(f"HTTP {resp.status_code}")
    try:
        body = resp.json()
    except Exception:
        body = resp.text
        log(f"响应：{body}")

    save_json(log_dir / "08a_上传原始题解结果.json", body, log)

    if resp.ok:
        log("原始题解上传成功")
        return True
    else:
        log(f"原始题解上传失败：{json.dumps(body, ensure_ascii=False)[:500]}")
        return False


def step8b_upload_solution(
    pid: str,
    solution: str,
    log,
    log_dir: Path,
) -> bool:
    """
    调用 POST /api/problem/upload_sol 上传修改后的题解
    """
    log(f"\n{'─'*40}")
    log("Step 8b: 上传修改后的题解")

    uname = os.environ["HYDRO_API_UNAME"]
    password = os.environ["HYDRO_API_PASSWORD"]

    payload = {
        "domainId": DOMAIN_ID,
        "uname": uname,
        "password": password,
        "pid": pid,
        "solution": solution,
    }

    url = f"{BASE_URL}/api/problem/upload_sol"
    try:
        resp = requests.post(
            url,
            json=payload,
            timeout=(10, 120),
            verify=True,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
    except requests.exceptions.RequestException as e:
        log(f"错误：上传题解请求失败：{e}")
        return False

    log(f"HTTP {resp.status_code}")
    try:
        body = resp.json()
    except Exception:
        body = resp.text
        log(f"响应：{body}")

    save_json(log_dir / "08b_上传题解结果.json", body, log)

    if resp.ok:
        log("题解上传成功")
        return True
    else:
        log(f"题解上传失败：{json.dumps(body, ensure_ascii=False)[:500]}")
        return False


# ============================================================
# Step 4 辅助：提取原始题面第一条样例
# ============================================================

def extract_first_sample_from_original(original_statement: str, log) -> dict | None:
    """
    从原始题面中提取第一条样例的输入输出。
    匹配格式：
      **输入**
      ```
      (...)
      ```
      **输出**
      ```
      (...)
      ```
    返回 {"input": "...", "output": "..."} 或 None
    """
    # 匹配 **输入** 后面紧跟的代码块
    input_pattern = r'\*\*输入\*\*\s*\n\s*```\s*\n(.*?)\n\s*```'
    output_pattern = r'\*\*输出\*\*\s*\n\s*```\s*\n(.*?)\n\s*```'

    input_match = re.search(input_pattern, original_statement, re.DOTALL)
    output_match = re.search(output_pattern, original_statement, re.DOTALL)

    if input_match and output_match:
        sample_input = input_match.group(1).strip()
        sample_output = output_match.group(1).strip()
        log(f"成功提取原始第一条样例，输入 {len(sample_input)} 字符，输出 {len(sample_output)} 字符")
        return {"input": sample_input, "output": sample_output}

    log("未从原始题面中提取到第一条样例（格式不匹配），将不使用格式参考")
    return None


# ============================================================
# Step 4: LLM 生成新样例
# ============================================================

STEP4_SYSTEM_PROMPT = load_prompt("step4_system.txt")


def step4_generate_samples(
    problem_data: dict,
    solution_code: str,
    original_statement: str,
    log,
    log_dir: Path,
    source: str = "agent",
) -> list | None:
    """
    LLM 生成新样例（2~4 条，含解释说明）
    problem_data: Step 3 生成的题面数据 {"title", "content", "input_description", "output_description"}
    original_statement: 原始题面，用于提取第一条样例作为格式参考
    返回 samples 列表或 None
    """
    log(f"\n{'─'*40}")
    log(f"Step 4: 生成新样例 (source={source})")
    if source == "agent":
        return load_samples_json(log_dir, log)

    client = create_llm_client(log)
    if client is None:
        return None

    # 构造题面描述（不含标题，只传给 LLM 用于理解题目逻辑）
    problem_desc = f"""# 题目内容
{problem_data['content']}

# 输入描述
{problem_data['input_description']}

# 输出描述
{problem_data['output_description']}"""

    # 从模板加载基础 user prompt
    step4_user_template = load_prompt("step4_user.txt")
    user_prompt = step4_user_template.format(
        problem_desc=problem_desc,
        solution_code=solution_code,
    )

    # 尝试提取原始第一条样例作为格式参考，提取成功则追加到 prompt 末尾
    original_sample = extract_first_sample_from_original(original_statement, log)
    if original_sample is not None:
        format_reference = f"""

## 原始样例格式参考（仅供格式参考，生成的新样例绝对不能与此样例完全相同）
以下是原始题面中第一条样例的输入输出格式，请参考其排版和风格：
**输入**
```
{original_sample['input']}
```
**输出**
```
{original_sample['output']}
```
注意：上述原始样例仅用于了解输入输出格式，你生成的新样例必须完全不同，不能照搬或简单修改此样例。"""
        user_prompt += format_reference

    # 验证器：检查 JSON 合法性及字段完整
    def validate_step4(response_text: str) -> bool:
        result = extract_json_from_llm_response(response_text, log)
        if result is None:
            return False
        if "samples" not in result or not isinstance(result["samples"], list):
            log("  验证失败：缺少 samples 字段或格式不正确")
            return False
        if len(result["samples"]) == 0:
            log("  验证失败：样例列表为空")
            return False
        return True

    response = call_llm_with_retry(
        client, STEP4_SYSTEM_PROMPT, user_prompt, log, "生成新样例",
        log_dir=log_dir, step_prefix="step4",
        validator=validate_step4,
    )
    if response is None:
        return None

    # 保存原始响应
    save_text(log_dir / "04_LLM生成的新样例_原始响应.txt", response, log)

    # 解析 JSON（validator 已保证可解析）
    result = extract_json_from_llm_response(response, log)

    samples = result["samples"]

    from forbid_orig_sample import original_forbidden, sample_hits_original

    forbidden = original_forbidden(original_statement or "")
    for i, sample in enumerate(samples, 1):
        hit = sample_hits_original(sample.get("input", ""), forbidden)
        if hit:
            log(f"错误：LLM 样例 {i} 仍使用原题面样例（{hit}）")
            return None

    log(f"生成 {len(samples)} 条样例")
    save_json(log_dir / "04_LLM生成的新样例.json", result, log)
    return samples


# ============================================================
# Step 5: 脚本拼接完整题面
# ============================================================

def fix_literal_newlines(text: str) -> str:
    """
    将字面量换行符 \\n（反斜杠+n 两个字符）替换为真正的换行符。

    LLM 在返回 JSON 时，经常把换行写成字面量 "\\n"（两个字符），
    而不是真正的换行符，导致 Markdown 渲染时不会换行。
    此函数把这种字面量 \\n 统一替换为真正的换行符。
    """
    return text.replace("\\n", "\n")


def step5_assemble_final_statement(
    problem_data: dict,
    samples: list,
    log,
    log_dir: Path,
) -> str | None:
    """
    将题面内容和样例按模板拼接为完整题面
    返回完整 Markdown 题面文本
    """
    log(f"\n{'─'*40}")
    log("Step 5: 拼接完整题面")

    content = fix_literal_newlines(problem_data["content"])
    input_desc = fix_literal_newlines(problem_data["input_description"])
    output_desc = fix_literal_newlines(problem_data["output_description"])

    # 构建题面（不含标题行，标题单独作为 API 参数传递）
    parts = []
    parts.append("# 题目内容\n")
    parts.append(content.strip())
    parts.append("\n\n# 输入描述\n")
    parts.append(input_desc.strip())
    parts.append("\n\n# 输出描述\n")
    parts.append(output_desc.strip())

    # 拼接样例
    for i, sample in enumerate(samples, 1):
        # LLM 可能返回数字类型的 input/output，统一转为字符串
        # 样例的 input/output 也可能把换行写成字面量 \n，同样需要转换
        sample_input = fix_literal_newlines(str(sample.get("input", "")).strip())
        sample_output = fix_literal_newlines(str(sample.get("output", "")).strip())
        # 说明文字同样可能含字面量 \n，需要转换
        sample_explanation = fix_literal_newlines(str(sample.get("explanation", "")).strip())
        parts.append(f"\n\n## 样例{i}\n")
        parts.append(f"\n**输入**\n\n```\n{sample_input}\n```\n")
        parts.append(f"\n**输出**\n\n```\n{sample_output}\n```\n")
        parts.append(f"\n**说明**\n\n{sample_explanation}")

    final_statement = "".join(parts)

    log(f"拼接完成，总长度：{len(final_statement)} 字符，样例数：{len(samples)}")
    save_text(log_dir / "05_拼接后的完整题面.md", final_statement, log)
    return final_statement


# ============================================================
# Step 6: 上传原始题面为附加文件
# ============================================================

def step6_upload_original_statement(
    pid: str,
    original_statement: str,
    original_title: str,
    log,
    log_dir: Path,
) -> bool:
    """
    调用 POST /api/problem/upload_testdata
    上传原始题面和原始标题为附加文件
    """
    log(f"\n{'─'*40}")
    log("Step 6: 上传原始题面和标题为附加文件")

    uname = os.environ["HYDRO_API_UNAME"]
    password = os.environ["HYDRO_API_PASSWORD"]

    payload = {
        "domainId": DOMAIN_ID,
        "uname": uname,
        "password": password,
        "pid": pid,
        "files": {
            "original_statement.md": original_statement,
            "original_title.txt": original_title,
        },
        "overwrite": True,
    }

    url = f"{BASE_URL}/api/problem/upload_testdata"
    try:
        resp = requests.post(
            url,
            json=payload,
            timeout=(10, 60),
            verify=True,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
    except requests.exceptions.RequestException as e:
        log(f"错误：上传原始题面请求失败：{e}")
        return False

    log(f"HTTP {resp.status_code}")
    try:
        body = resp.json()
    except Exception:
        body = resp.text
        log(f"响应：{body}")

    save_json(log_dir / "06_上传原始题面结果.json", body, log)

    if resp.ok:
        log("原始题面上传成功")
        return True
    else:
        log(f"原始题面上传失败：{json.dumps(body, ensure_ascii=False)[:500]}")
        return False


# ============================================================
# Step 7: 上传新题面和新标题
# ============================================================

def step7_upload_new_problem(
    pid: str,
    title: str,
    content: str,
    log,
    log_dir: Path,
) -> bool:
    """
    调用 POST /api/problem/update
    上传新标题和新题面（只传 title 和 content，不改其他属性）
    """
    log(f"\n{'─'*40}")
    log("Step 7: 上传新题面和新标题")

    uname = os.environ["HYDRO_API_UNAME"]
    password = os.environ["HYDRO_API_PASSWORD"]

    payload = {
        "domainId": DOMAIN_ID,
        "uname": uname,
        "password": password,
        "pid": pid,
        "title": title,
        "content": content,
    }

    url = f"{BASE_URL}/api/problem/update"
    try:
        resp = requests.post(
            url,
            json=payload,
            timeout=(10, 60),
            verify=True,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
    except requests.exceptions.RequestException as e:
        log(f"错误：上传新题面请求失败：{e}")
        return False

    log(f"HTTP {resp.status_code}")
    try:
        body = resp.json()
    except Exception:
        body = resp.text
        log(f"响应：{body}")

    save_json(log_dir / "07_上传新题面结果.json", body, log)

    if resp.ok:
        log("新题面上传成功")
        return True
    else:
        log(f"新题面上传失败：{json.dumps(body, ensure_ascii=False)[:500]}")
        return False


# ============================================================
# 主流程
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="OJ 题目重写与上传自动化脚本"
    )
    parser.add_argument(
        "--pid",
        required=True,
        help="题目 ID，例如 P1001",
    )
    parser.add_argument(
        "--mode",
        type=int,
        default=0,
        choices=[0, 1, 2, 3, 4, 5, 6],
        help="0=完整流程, 1=交互暂停, 2=仅获取, 3=仅生成/拼接, 4=仅上传, 5=重做题解并上传, 6=读取Agent产物拼接并上传",
    )
    parser.add_argument(
        "--source",
        choices=["agent", "deepseek"],
        default="agent",
        help="题面/题解/样例来源：agent=读取 log 产物（默认），deepseek=调用 DeepSeek API",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="强制覆盖模式：先删除 log/{pid}/ 目录再运行",
    )
    args = parser.parse_args()

    pid = args.pid.upper()
    mode = args.mode
    force = args.force
    source = args.source

    log_dir = get_log_dir(pid)
    backup_dir = get_script_dir() / "backup" / pid

    # 检查 log 目录是否已存在
    if log_dir.exists():
        if force:
            shutil.rmtree(log_dir)
            print(f"强制覆盖：已删除旧目录 {log_dir}")
        elif mode in KEEP_LOG_MODES:
            pass
        else:
            summary_path = log_dir / "运行汇总.json"
            already_done = False
            if summary_path.exists():
                try:
                    summary = json.loads(summary_path.read_text(encoding="utf-8"))
                    already_done = bool(summary.get("overall_success"))
                except Exception:
                    already_done = False
            if already_done:
                print(f"该题目已成功处理过，跳过（{log_dir}）")
                print(f"如需重新处理，请使用 --force 参数覆盖。")
                sys.exit(0)
            if source == "deepseek":
                shutil.rmtree(log_dir)
                print(f"上次运行未完全成功，已清理旧目录 {log_dir}，重新运行")
            else:
                print(f"保留未完成 log，供 Agent 补全产物：{log_dir}")

    log = init_logger(log_dir)

    log(f"脚本启动")
    log(f"  PID: {pid}")
    log(f"  模式: {mode}")
    log(f"  来源: {source}")
    log(f"  BASE_URL: {BASE_URL}")
    log(f"  Log 目录: {log_dir}")

    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 检查环境变量
    if not check_env_vars(log, source):
        sys.exit(EXIT_ENV_ERROR)

    require_https(BASE_URL)

    # ========================================
    # 模式 4：仅上传数据
    # ========================================
    if mode == 4:
        log("\n模式 4：仅上传数据")

        # 读取已保存的拼接后题面
        assembled_path = log_dir / "05_拼接后的完整题面.md"
        if not assembled_path.exists():
            log(f"错误：找不到 {assembled_path}，请先运行模式 3 生成数据")
            sys.exit(EXIT_MISSING_FILE)

        content = assembled_path.read_text(encoding="utf-8")
        log(f"已读取拼接后的题面，长度：{len(content)} 字符")

        # 读取标题
        problem_json_path = log_dir / "03_LLM生成的新题面.json"
        if not problem_json_path.exists():
            log(f"错误：找不到 {problem_json_path}，请先运行模式 3 生成数据")
            sys.exit(EXIT_MISSING_FILE)

        try:
            problem_data = json.loads(problem_json_path.read_text(encoding="utf-8"))
            title = problem_data.get("title", "")
        except Exception as e:
            log(f"错误：读取标题失败：{e}")
            sys.exit(EXIT_MISSING_FILE)

        if not title:
            log("错误：标题为空")
            sys.exit(EXIT_MISSING_FILE)
        log(f"标题: {title}")

        # 读取原始题面
        original_path = log_dir / "01_原始题面.md"
        if not original_path.exists():
            log(f"错误：找不到 {original_path}，请先运行模式 2/3 获取数据")
            sys.exit(EXIT_MISSING_FILE)

        original_statement = original_path.read_text(encoding="utf-8")
        log(f"已读取原始题面，长度：{len(original_statement)} 字符")

        # 读取原始标题
        original_title_path = log_dir / "01_原始标题.txt"
        original_title = ""
        if original_title_path.exists():
            original_title = original_title_path.read_text(encoding="utf-8").strip()
            log(f"已读取原始标题: {original_title}")

        # 如果原始标题以"第x题-"开头，提取前缀加到新标题前面
        prefix_match = re.match(r'^(第\d+题-)', original_title)
        if prefix_match:
            prefix = prefix_match.group(1)
            title = f"{prefix}{title}"
            log(f"原始标题前缀: {prefix}")
            log(f"最终标题: {title}")

        pause_if_mode1(mode, "即将上传原始题面（Step 6）")
        if not step6_upload_original_statement(pid, original_statement, original_title, log, log_dir):
            log("Step 6 失败，终止")
            sys.exit(EXIT_STEP6_FAILED)

        pause_if_mode1(mode, "即将上传新题面（Step 7）")
        if not step7_upload_new_problem(pid, title, content, log, log_dir):
            log("Step 7 失败，终止")
            sys.exit(EXIT_STEP7_FAILED)

        # 检查是否有修改后的题解需要上传
        new_solution_path = log_dir / "03.5_修改后的题解.md"
        if new_solution_path.exists():
            # 读取原始题解
            original_solution_path = log_dir / "02_原始完整题解.md"
            if not original_solution_path.exists():
                log(f"错误：找不到 {original_solution_path}")
                sys.exit(EXIT_MISSING_FILE)
            original_solution = original_solution_path.read_text(encoding="utf-8")

            pause_if_mode1(mode, "即将上传原始题解文件（Step 8a）")
            if not step8a_upload_original_solution(pid, original_solution, log, log_dir):
                log("Step 8a 失败，终止")
                sys.exit(EXIT_STEP8_FAILED)

            pause_if_mode1(mode, "即将上传修改后的题解（Step 8b）")
            new_solution = new_solution_path.read_text(encoding="utf-8")
            if not step8b_upload_solution(pid, new_solution, log, log_dir):
                log("Step 8b 失败，终止")
                sys.exit(EXIT_STEP8_FAILED)
        else:
            log("\n题解无需修改，跳过上传")

        # 模式 4 汇总
        summary = {
            "pid": pid,
            "mode": mode,
            "force": force,
            "start_time": start_time,
            "end_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "new_title": title,
            "mode4_upload": True,
            "overall_success": True,
        }
        save_json(log_dir / "运行汇总.json", summary, log)

        log("\n全部上传完成！")
        log(f"执行完毕: {summary['end_time']}")
        if mode == 1:
            input("\n脚本执行完毕，按回车键退出...")
        return

    # ========================================
    # 模式 6：读取 Agent 产物，拼接并上传
    # ========================================
    if mode == 6:
        log("\n模式 6：读取 Agent 产物，拼接并上传")
        missing = missing_agent_artifacts(log_dir)
        if missing:
            log("错误：缺少以下 Agent 产物，无法拼接上传：")
            for name in missing:
                log(f"  - {name}")
            sys.exit(EXIT_WAITING_AGENT)

        original_path = log_dir / "01_原始题面.md"
        original_title_path = log_dir / "01_原始标题.txt"
        original_solution_path = log_dir / "02_原始完整题解.md"
        if not original_path.exists() or not original_title_path.exists() or not original_solution_path.exists():
            log("错误：缺少原始题面/标题/题解，请先运行 --mode 2")
            sys.exit(EXIT_MISSING_FILE)

        original_statement = original_path.read_text(encoding="utf-8")
        original_title = original_title_path.read_text(encoding="utf-8").strip()
        full_solution_md = original_solution_path.read_text(encoding="utf-8")

        problem_data = load_problem_json(log_dir, log)
        samples = load_samples_json(log_dir, log)
        new_solution_md = load_solution_markdown(log_dir, log)
        if problem_data is None or samples is None or new_solution_md is None:
            sys.exit(EXIT_WAITING_AGENT)

        final_statement = step5_assemble_final_statement(problem_data, samples, log, log_dir)
        if final_statement is None:
            log("Step 5 失败，终止")
            sys.exit(EXIT_STEP5_FAILED)

        title = apply_title_prefix(problem_data["title"], original_title, log)

        if not step6_upload_original_statement(pid, original_statement, original_title, log, log_dir):
            log("Step 6 失败，终止")
            sys.exit(EXIT_STEP6_FAILED)
        if not step7_upload_new_problem(pid, title, final_statement, log, log_dir):
            log("Step 7 失败，终止")
            sys.exit(EXIT_STEP7_FAILED)
        if not step8a_upload_original_solution(pid, full_solution_md, log, log_dir):
            log("Step 8a 失败，终止")
            sys.exit(EXIT_STEP8_FAILED)
        if not step8b_upload_solution(pid, new_solution_md, log, log_dir):
            log("Step 8b 失败，终止")
            sys.exit(EXIT_STEP8_FAILED)

        summary = {
            "pid": pid,
            "mode": mode,
            "source": source,
            "force": force,
            "start_time": start_time,
            "end_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "new_title": title,
            "mode6_agent_upload": True,
            "overall_success": True,
        }
        save_json(log_dir / "运行汇总.json", summary, log)
        log("\nAgent 产物拼接并上传完成！")
        log(f"执行完毕: {summary['end_time']}")
        return

    # ========================================
    # 模式 5：仅重新生成模板题解并上传
    # 读取已有 log 数据，重新运行 Step 3.5 生成模板格式题解（## 解题思路 / ## 复杂度分析 / ## 代码实现 三语言），然后上传
    # ========================================
    if mode == 5:
        log("\n模式 5：仅重新生成模板题解并上传")

        # 读取已有新题面 JSON 作为 problem_data
        problem_json_path = log_dir / "03_LLM生成的新题面.json"
        if not problem_json_path.exists():
            log(f"错误：找不到 {problem_json_path}，请先运行完整流程生成数据")
            sys.exit(EXIT_MISSING_FILE)
        try:
            problem_data = json.loads(problem_json_path.read_text(encoding="utf-8"))
        except Exception as e:
            log(f"错误：读取新题面 JSON 失败：{e}")
            sys.exit(EXIT_MISSING_FILE)

        # 读取原始完整题解
        original_solution_path = log_dir / "02_原始完整题解.md"
        if not original_solution_path.exists():
            log(f"错误：找不到 {original_solution_path}")
            sys.exit(EXIT_MISSING_FILE)
        full_solution_md = original_solution_path.read_text(encoding="utf-8")

        # Step 3.5: 重新生成模板格式题解
        new_solution_md, step35_ok = step35_check_and_fix_solution(
            problem_data, full_solution_md, log, log_dir, source=source
        )
        if not step35_ok:
            log("Step 3.5 失败，终止")
            sys.exit(EXIT_STEP35_FAILED)
        if new_solution_md is None:
            log("错误：Step 3.5 未生成新题解")
            sys.exit(EXIT_STEP35_FAILED)

        pause_if_mode1(mode, "Step 3.5 完成，请检查模板题解生成结果")

        # Step 8a: 上传原始题解
        pause_if_mode1(mode, "即将上传原始题解文件（Step 8a）")
        if not step8a_upload_original_solution(pid, full_solution_md, log, log_dir):
            log("Step 8a 失败，终止")
            sys.exit(EXIT_STEP8_FAILED)

        # Step 8b: 上传新题解
        pause_if_mode1(mode, "即将上传模板题解（Step 8b）")
        if not step8b_upload_solution(pid, new_solution_md, log, log_dir):
            log("Step 8b 失败，终止")
            sys.exit(EXIT_STEP8_FAILED)

        # 模式 5 汇总
        summary = {
            "pid": pid,
            "mode": mode,
            "force": force,
            "start_time": start_time,
            "end_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "new_title": problem_data.get("title", ""),
            "mode5_regenerate_solution": True,
            "step35_modified": True,
            "step8_upload_solution": True,
            "overall_success": True,
        }
        save_json(log_dir / "运行汇总.json", summary, log)

        log("\n模板题解重新生成并上传完成！")
        log(f"执行完毕: {summary['end_time']}")
        if mode == 1:
            input("\n脚本执行完毕，按回车键退出...")
        return

    # ========================================
    # 模式 2/3/0：都需要获取数据
    # ========================================

    # 检查备份目录是否存在且完整
    backup_statement = backup_dir / "01_原始题面.md"
    backup_title_file = backup_dir / "01_原始标题.txt"
    backup_solution_file = backup_dir / "02_原始完整题解.md"
    backup_available = (
        backup_dir.exists()
        and backup_statement.exists()
        and backup_title_file.exists()
        and backup_solution_file.exists()
    )

    if backup_available:
        # 优先从备份目录获取原始数据
        log("备份数据完整，优先从备份获取原始数据")
        original_statement = backup_statement.read_text(encoding="utf-8")
        original_title = backup_title_file.read_text(encoding="utf-8").strip()
        full_solution_md = backup_solution_file.read_text(encoding="utf-8")
        solution_code = extract_code_block(full_solution_md)
        if solution_code is None:
            log("警告：备份的题解中未找到有效代码块，使用全文")
            solution_code = full_solution_md
        log(f"从备份加载原始题面，长度：{len(original_statement)} 字符")
        log(f"从备份加载原始标题: {original_title}")
        log(f"从备份加载题解，Python 代码长度：{len(solution_code)} 字符")
        # 同步保存到 log 目录
        save_text(log_dir / "01_原始题面.md", original_statement, log)
        save_text(log_dir / "01_原始标题.txt", original_title, log)
        save_text(log_dir / "02_题解代码.py", solution_code, log)
        save_text(log_dir / "02_原始完整题解.md", full_solution_md, log)
    else:
        # 从 API 获取数据
        # Step 1: 获取原始题面
        step1_result = step1_fetch_problem(pid, log, log_dir)
        if step1_result is None:
            log("Step 1 失败，终止")
            sys.exit(EXIT_STEP1_FAILED)
        original_statement, original_title = step1_result

        pause_if_mode1(mode, "Step 1 完成，请检查原始题面")

        # Step 2: 获取题解代码
        step2_result = step2_fetch_solution(pid, log, log_dir)
        if step2_result is None:
            log("Step 2 失败，终止")
            sys.exit(EXIT_STEP2_FAILED)
        solution_code, full_solution_md = step2_result

        pause_if_mode1(mode, "Step 2 完成，请检查题解代码")

        # 备份原始数据（仅在备份目录不存在时执行）
        if not backup_dir.exists():
            backup_dir.mkdir(parents=True, exist_ok=True)
            save_text(backup_statement, original_statement, log)
            save_text(backup_title_file, original_title, log)
            save_text(backup_solution_file, full_solution_md, log)
            log(f"原始数据已备份到: {backup_dir}")
        else:
            log(f"备份目录已存在，跳过备份: {backup_dir}")

    # 模式 2：仅获取数据，到此结束
    if mode == 2:
        log("\n模式 2：数据获取完成，退出")
        log(f"执行完毕: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return

    # ========================================
    # 模式 3/0：继续生成数据
    # ========================================

    if source == "agent":
        missing = missing_agent_artifacts(log_dir)
        if missing:
            log("等待 Cursor Agent 写入下列产物后，再运行 --mode 6 拼接上传：")
            for name in missing:
                log(f"  - log/{pid}/{name}")
            log("规则见 fix/AGENT_REWRITE.md")
            sys.exit(EXIT_WAITING_AGENT)

    # Step 3: 生成新题面
    problem_data = step3_generate_problem_statement(
        original_statement, solution_code, log, log_dir, source=source
    )
    if problem_data is None:
        log("Step 3 失败，终止")
        sys.exit(EXIT_STEP3_FAILED if source == "deepseek" else EXIT_WAITING_AGENT)

    pause_if_mode1(mode, "Step 3 完成，请检查生成的新题面")

    # Step 3.5: 生成模板题解
    new_solution_md, step35_ok = step35_check_and_fix_solution(
        problem_data, full_solution_md, log, log_dir, source=source
    )
    if not step35_ok:
        log("Step 3.5 失败，终止")
        sys.exit(EXIT_STEP35_FAILED if source == "deepseek" else EXIT_WAITING_AGENT)
    solution_modified = new_solution_md is not None
    if solution_modified:
        log("题解已根据新题面进行适配修改")
    else:
        log("题解与新题面无冲突，无需修改")

    pause_if_mode1(mode, "Step 3.5 完成，请检查题解修改结果")

    # Step 4: 生成新样例
    samples = step4_generate_samples(
        problem_data, solution_code, original_statement, log, log_dir, source=source
    )
    if samples is None:
        log("Step 4 失败，终止")
        sys.exit(EXIT_STEP4_FAILED if source == "deepseek" else EXIT_WAITING_AGENT)

    pause_if_mode1(mode, "Step 4 完成，请检查生成的新样例")

    # Step 5: 拼接完整题面
    final_statement = step5_assemble_final_statement(problem_data, samples, log, log_dir)
    if final_statement is None:
        log("Step 5 失败，终止")
        sys.exit(EXIT_STEP5_FAILED)

    pause_if_mode1(mode, "Step 5 完成，请检查拼接后的完整题面")

    # 模式 3：仅生成数据，到此结束
    if mode == 3:
        log("\n模式 3：数据生成完成，退出")
        log(f"执行完毕: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        # 写入运行汇总，标记数据生成成功，便于后续模式 4 直接上传
        summary = {
            "pid": pid,
            "mode": mode,
            "force": force,
            "start_time": start_time,
            "end_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "new_title": problem_data.get("title", ""),
            "mode3_generated": True,
            "overall_success": True,
        }
        save_json(log_dir / "运行汇总.json", summary, log)
        return

    # ========================================
    # 模式 0：继续上传
    # ========================================

    title = problem_data["title"]

    # 如果原始标题以"第x题-"开头，提取前缀加到新标题前面
    prefix_match = re.match(r'^(第\d+题-)', original_title)
    if prefix_match:
        prefix = prefix_match.group(1)
        title = f"{prefix}{title}"
        log(f"原始标题前缀: {prefix}")
        log(f"最终标题: {title}")

    pause_if_mode1(mode, "即将上传原始题面（Step 6）")
    if not step6_upload_original_statement(pid, original_statement, original_title, log, log_dir):
        log("Step 6 失败，终止")
        sys.exit(EXIT_STEP6_FAILED)

    pause_if_mode1(mode, "即将上传新题面（Step 7）")
    if not step7_upload_new_problem(pid, title, final_statement, log, log_dir):
        log("Step 7 失败，终止")
        sys.exit(EXIT_STEP7_FAILED)

    # Step 8: 上传题解（仅在题解有修改时）
    if solution_modified:
        pause_if_mode1(mode, "即将上传原始题解文件（Step 8a）")
        if not step8a_upload_original_solution(pid, full_solution_md, log, log_dir):
            log("Step 8a 失败，终止")
            sys.exit(EXIT_STEP8_FAILED)

        pause_if_mode1(mode, "即将上传修改后的题解（Step 8b）")
        if not step8b_upload_solution(pid, new_solution_md, log, log_dir):
            log("Step 8b 失败，终止")
            sys.exit(EXIT_STEP8_FAILED)
    else:
        log("\n题解无需修改，跳过上传")

    # 汇总结果
    summary = {
        "pid": pid,
        "mode": mode,
        "force": force,
        "start_time": start_time,
        "end_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "new_title": title,
        "steps": {
            "step1_fetch_problem": True,
            "step2_fetch_solution": True,
            "step3_generate_statement": True,
            "step35_check_solution": step35_ok,
            "step35_modified": solution_modified,
            "step4_generate_samples": True,
            "step5_assemble": True,
            "step6_upload_original_statement": True,
            "step7_upload_new_problem": True,
            "step8_upload_solution": solution_modified,
        },
        "overall_success": True,
    }

    log("\n" + "="*60)
    log("全部完成！")
    log(f"  题目: {pid}")
    log(f"  新标题: {title}")
    log(f"  Log 目录: {log_dir}")
    log(f"执行完毕: {summary['end_time']}")

    save_json(log_dir / "运行汇总.json", summary, log)

    if mode == 1:
        input("\n脚本执行完毕，按回车键退出...")


if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        sys.exit(e.code if e.code is not None else 1)
    except Exception:
        print(f"\n未捕获的异常:\n{traceback.format_exc()}")
        sys.exit(99)
