import base64
import os
import sys
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import API_BASE, API_KEY, MODEL_ID

# 全局 session，复用连接并跳过 SSL 验证（针对自建/代理 API）
session = requests.Session()
session.verify = False
# 禁用 SSL 警告
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 路径配置
INPUT_DIR = os.path.join(os.path.dirname(__file__), "input")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "output.txt")
PROMPT_FILE = os.path.join(os.path.dirname(__file__), "prompt.txt")


def encode_image_to_base64(image_path: str) -> str:
    """将图片文件编码为 base64 字符串"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def get_image_mime_type(image_path: str) -> str:
    """根据扩展名返回 MIME 类型"""
    ext = os.path.splitext(image_path)[1].lower()
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    return mime_map.get(ext, "image/png")


def build_messages(prompt: str, image_paths: list[str]) -> list[dict]:
    """
    构建包含文本和图片的 messages
    使用 OpenAI 兼容的多模态格式
    """
    content = [{"type": "text", "text": prompt}]

    for img_path in image_paths:
        b64 = encode_image_to_base64(img_path)
        mime = get_image_mime_type(img_path)
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:{mime};base64,{b64}"
            }
        })

    return [{"role": "user", "content": content}]


def call_api(messages: list[dict]) -> str:
    """调用 API，返回模型响应文本"""
    url = f"{API_BASE.rstrip('/')}/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL_ID,
        "messages": messages,
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            resp = session.post(url, headers=headers, json=payload, timeout=300)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except requests.exceptions.SSLError as e:
            print(f"SSL 错误（第 {attempt + 1}/{max_retries} 次尝试）: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                raise
        except requests.exceptions.RequestException as e:
            print(f"请求错误（第 {attempt + 1}/{max_retries} 次尝试）: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                raise


def main():
    # 读取提示词
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        prompt = f.read()

    # 收集 input 目录下所有图片（按文件名排序）
    image_paths = sorted([
        os.path.join(INPUT_DIR, f)
        for f in os.listdir(INPUT_DIR)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp"))
    ])

    if not image_paths:
        print("input 目录中没有找到图片文件")
        return

    print(f"找到 {len(image_paths)} 张图片，正在调用 API ...")

    # 构建消息并调用 API
    messages = build_messages(prompt, image_paths)
    result = call_api(messages)

    # 输出到文件
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"完成！结果已写入 {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
