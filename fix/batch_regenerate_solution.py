"""
批量重新生成模板题解并上传（多进程并发版）：
读取 batch_progress.json 中已成功（status=success）的 PID，并发调用
rewrite_and_upload.py --pid {pid} --mode 5，为每道题重新生成符合固定模板格式
（## 解题思路 / ## 复杂度分析 / ## 代码实现 含 Python/Java/C++ 三语言）的题解并上传。

支持 Ctrl+C 安全中断，运行状态实时写入进度文件。

用法：
  python batch_regenerate_solution.py              # 默认 4 并发
  python batch_regenerate_solution.py -w 8         # 8 并发
"""
from __future__ import annotations

import argparse
import json
import multiprocessing
import random
import signal
import subprocess
import sys
import threading
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REWRITE_SCRIPT = SCRIPT_DIR / "rewrite_and_upload.py"
SRC_PROGRESS_FILE = SCRIPT_DIR / "log" / "batch_progress.json"
PROGRESS_FILE = SCRIPT_DIR / "log" / "batch_solution_progress.json"
SUMMARY_FILE = SCRIPT_DIR / "log" / "batch_solution_summary.txt"
SUBPROCESS_TIMEOUT = 900   # 每个子进程最长 15 分钟
STARTUP_JITTER_MAX = 3.0   # 子进程启动最大随机延迟（秒），避免同时冲击 API


class ProgressTracker:
    """线程安全的进度跟踪器"""

    def __init__(self, pids: list[str]):
        self.lock = threading.Lock()
        self.results = {}
        self.total = len(pids)
        self.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.interrupted = False

    def mark_start(self, pid: str):
        with self.lock:
            self.results[pid] = {"status": "running", "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "error": None}
            self._write_locked()

    def mark_success(self, pid: str):
        with self.lock:
            self.results[pid] = {"status": "success", "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "error": None}
            self._write_locked()

    def mark_fail(self, pid: str, error: str):
        with self.lock:
            self.results[pid] = {"status": "fail", "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "error": error}
            self._write_locked()

    def mark_interrupted(self):
        with self.lock:
            self.interrupted = True
            self._write_locked()

    def _write_locked(self):
        data = {
            "total": self.total,
            "start_time": self.start_time,
            "interrupted": self.interrupted,
            "results": self.results,
        }
        PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def get_summary(self, max_workers: int) -> str:
        done = [v for v in self.results.values() if v["status"] in ("success", "fail")]
        success = sum(1 for v in self.results.values() if v["status"] == "success")
        fail = sum(1 for v in self.results.values() if v["status"] == "fail")
        running = sum(1 for v in self.results.values() if v["status"] == "running")
        lines = [
            "=" * 60,
            "模板题解重新生成批量执行汇总",
            "=" * 60,
            f"开始时间: {self.start_time}",
            f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"并发数: {max_workers}",
            f"总题目数: {self.total}",
            f"成功: {success}",
            f"失败: {fail}",
            f"运行中: {running}",
            f"中断: {'是' if self.interrupted else '否'}",
            "-" * 60,
        ]
        if fail:
            lines.append("失败列表:")
            for pid, v in self.results.items():
                if v["status"] == "fail":
                    lines.append(f"  {pid}: {v.get('error')}")
        return "\n".join(lines)


def process_one_pid(args: tuple) -> tuple[str, str, str | None]:
    """
    在子进程中执行单个题目的模板题解重新生成（mode 5）。
    返回 (pid, status, error_or_None)
    """
    pid, script_dir, rewrite_script, timeout = args

    # 子进程忽略 SIGINT，由主进程统一管理
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    # 随机延迟，避免多个子进程同时冲击 API
    time.sleep(random.uniform(0, STARTUP_JITTER_MAX))

    try:
        result = subprocess.run(
            [sys.executable, str(rewrite_script), "--pid", pid, "--mode", "5"],
            cwd=str(script_dir),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode == 0:
            return (pid, "success", None)
        else:
            return (pid, "fail", f"返回码 {result.returncode}")
    except subprocess.TimeoutExpired:
        return (pid, "fail", f"超时 {timeout}s")
    except Exception as e:
        return (pid, "fail", str(e))


def _shutdown_executor(executor, wait=False):
    """安全关闭 executor，兼容 Python < 3.9（无 cancel_futures 参数）"""
    try:
        executor.shutdown(wait=wait, cancel_futures=True)
    except TypeError:
        executor.shutdown(wait=wait)


def main():
    parser = argparse.ArgumentParser(description="批量重新生成模板题解并上传（多进程并发）")
    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=4,
        help="并发进程数（默认 4）",
    )
    args = parser.parse_args()
    max_workers = args.workers

    if not SRC_PROGRESS_FILE.exists():
        print(f"错误：找不到 {SRC_PROGRESS_FILE}，请先运行 batch_rewrite.py")
        sys.exit(1)

    src = json.loads(SRC_PROGRESS_FILE.read_text(encoding="utf-8"))
    results = src.get("results", {})
    # 只取已成功（status=success）的 PID
    pids = [pid for pid, v in results.items() if v.get("status") == "success"]
    if not pids:
        print("错误：batch_progress.json 中没有成功完成的 PID")
        sys.exit(1)

    print(f"共 {len(pids)} 个已成功题目待重新生成模板题解")
    print(f"并发数: {max_workers}")
    print(f"进度文件: {PROGRESS_FILE}")
    print()

    tracker = ProgressTracker(pids)

    tasks = [(pid, SCRIPT_DIR, REWRITE_SCRIPT, SUBPROCESS_TIMEOUT) for pid in pids]

    interrupt_event = threading.Event()
    executor = None

    def on_sigint(signum, frame):
        interrupt_event.set()
        signal.signal(signal.SIGINT, signal.SIG_DFL)

    original_handler = signal.signal(signal.SIGINT, on_sigint)

    executor = ProcessPoolExecutor(max_workers=max_workers)

    try:
        futures = {executor.submit(process_one_pid, task): task[0] for task in tasks}

        for future in as_completed(futures):
            if interrupt_event.is_set():
                print(f"\n\n收到 Ctrl+C，正在终止所有子进程...")
                tracker.mark_interrupted()
                _shutdown_executor(executor, wait=False)
                for f in futures:
                    f.cancel()
                break

            pid = futures[future]
            try:
                pid_result, status, error = future.result()
                if status == "success":
                    print(f"[完成] {pid}: 成功", flush=True)
                    tracker.mark_success(pid)
                else:
                    print(f"[完成] {pid}: 失败 ({error})", flush=True)
                    tracker.mark_fail(pid, error)
            except Exception as e:
                print(f"[完成] {pid}: 异常 ({e})", flush=True)
                tracker.mark_fail(pid, str(e))

        summary = tracker.get_summary(max_workers)
        SUMMARY_FILE.write_text(summary, encoding="utf-8")
        print(f"\n{summary}")
        print(f"\n汇总已保存到: {SUMMARY_FILE}")

    finally:
        signal.signal(signal.SIGINT, original_handler)
        if executor is not None:
            _shutdown_executor(executor, wait=False)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
