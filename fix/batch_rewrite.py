"""
批量重写脚本（多进程并发版）：读取 all.txt，并发调用 rewrite_and_upload.py
支持 Ctrl+C 安全中断，运行状态实时写入进度文件。

用法：
  python batch_rewrite.py              # 默认 4 并发
  python batch_rewrite.py -w 8         # 8 并发
  python batch_rewrite.py --workers 8  # 同上
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
ALL_TXT = SCRIPT_DIR / "all.txt"
REWRITE_SCRIPT = SCRIPT_DIR / "rewrite_and_upload.py"
PROGRESS_FILE = SCRIPT_DIR / "log" / "batch_progress.json"
SUBPROCESS_TIMEOUT = 900   # 每个子进程最长 15 分钟
STARTUP_JITTER_MAX = 3.0   # 子进程启动最大随机延迟（秒），避免同时冲击 API


class ProgressTracker:
    """线程安全的进度跟踪器"""

    def __init__(self, pids: list[str]):
        self.pids = pids
        self.lock = threading.Lock()
        self.results: dict[str, dict] = {}            # pid -> {status, time, error}
        self.running: list[str] = []                   # 当前正在运行的 pid
        self.interrupted = False
        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._write()

    def mark_start(self, pid: str):
        with self.lock:
            self.results[pid] = {"status": "running", "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "error": None}
            if pid not in self.running:
                self.running.append(pid)
            self._write_locked()

    def mark_success(self, pid: str):
        with self.lock:
            self.results[pid] = {"status": "success", "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "error": None}
            if pid in self.running:
                self.running.remove(pid)
            self._write_locked()

    def mark_fail(self, pid: str, error: str):
        with self.lock:
            self.results[pid] = {"status": "fail", "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "error": error}
            if pid in self.running:
                self.running.remove(pid)
            self._write_locked()

    def mark_waiting(self, pid: str, error: str = "等待 Agent 产物"):
        with self.lock:
            self.results[pid] = {"status": "waiting", "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "error": error}
            if pid in self.running:
                self.running.remove(pid)
            self._write_locked()

    def mark_interrupted(self):
        with self.lock:
            self.interrupted = True
            for pid in list(self.running):
                if pid in self.results and self.results[pid]["status"] == "running":
                    self.results[pid] = {"status": "interrupted", "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "error": "用户 Ctrl+C 中断"}
            self.running[:] = []
            self._write_locked()

    def _write_locked(self):
        """仅在持有 lock 时调用"""
        data = {
            "start_time": self.start_time,
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "running": list(self.running),
            "total": len(self.pids),
            "interrupted": self.interrupted,
            "results": dict(self.results),
        }
        PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def _write(self):
        """初始化写入"""
        with self.lock:
            self._write_locked()

    def get_summary(self, max_workers: int) -> str:
        with self.lock:
            results = dict(self.results)
            pids_snapshot = list(self.pids)
        success = [p for p, r in results.items() if r["status"] == "success"]
        fail = [p for p, r in results.items() if r["status"] == "fail"]
        waiting = [p for p, r in results.items() if r["status"] == "waiting"]
        interrupted = [p for p, r in results.items() if r["status"] == "interrupted"]
        pending = [p for p in pids_snapshot if p not in results]

        lines = [
            "批量执行汇总",
            "=" * 60,
            f"并发数: {max_workers}",
            f"开始时间: {self.start_time}",
            f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"总数: {len(pids_snapshot)}",
            f"成功: {len(success)}",
            f"失败: {len(fail)}",
            f"等待Agent: {len(waiting)}",
            f"中断: {len(interrupted)}",
            f"未处理: {len(pending)}",
            "",
            f"成功列表: {', '.join(success) if success else '无'}",
            f"失败列表: {', '.join(fail) if fail else '无'}",
            f"等待Agent列表: {', '.join(waiting) if waiting else '无'}",
            f"中断列表: {', '.join(interrupted) if interrupted else '无'}",
            f"未处理列表: {', '.join(pending) if pending else '无'}",
        ]
        return "\n".join(lines)


def process_one_pid(args: tuple) -> tuple[str, str, str | None]:
    """
    在子进程中执行单个题目的重写。
    返回 (pid, status, error_or_None)
    注意：multiprocessing 中信号处理需要重新初始化。
    """
    pid, script_dir, rewrite_script, timeout, force, mode, source = args

    # 子进程忽略 SIGINT，由主进程统一管理
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    # 随机延迟，避免多个子进程同时冲击 API
    time.sleep(random.uniform(0, STARTUP_JITTER_MAX))

    try:
        cmd = [sys.executable, str(rewrite_script), "--pid", pid, "--mode", str(mode), "--source", source]
        if force:
            cmd.append("--force")
        result = subprocess.run(
            cmd,
            cwd=str(script_dir),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        # rewrite_and_upload 会自己保存日志到 log/{pid}/，此处不输出到控制台
        if result.returncode == 0:
            return (pid, "success", None)
        elif result.returncode == 22:
            return (pid, "waiting", "等待 Agent 写入 03/03.5/04")
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
        # Python < 3.9 不支持 cancel_futures
        executor.shutdown(wait=wait)


def main():
    parser = argparse.ArgumentParser(description="批量重写 OJ 题目（多进程并发）")
    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=4,
        help="并发进程数（默认 4）",
    )
    parser.add_argument(
        "--mode",
        type=int,
        default=2,
        choices=[0, 2, 3, 4, 5, 6],
        help="传给 rewrite_and_upload.py 的模式。Agent 工作流：先 2 拉取，Agent 写产物，再 6 上传。默认 2",
    )
    parser.add_argument(
        "--source",
        choices=["agent", "deepseek"],
        default="agent",
        help="题面来源，默认 agent（不调用 DeepSeek）",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="强制覆盖模式：即使题目已成功处理过也重新运行（传递给 rewrite_and_upload.py）",
    )
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    max_workers = args.workers
    force = args.force
    mode = args.mode
    source = args.source

    if not ALL_TXT.exists():
        print(f"错误：找不到 {ALL_TXT}，请先运行 extract_pids.py")
        sys.exit(1)

    pids = [
        line.strip().lstrip("\ufeff")
        for line in ALL_TXT.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]
    print(f"共 {len(pids)} 个题目待处理")
    print(f"并发数: {max_workers}")
    print(f"模式: {mode}  来源: {source}")
    print(f"进度文件: {PROGRESS_FILE}")
    print()

    tracker = ProgressTracker(pids)

    # 任务列表（全部 pid 都执行，由 rewrite_and_upload.py 内部处理 --force 逻辑）
    tasks = [(pid, SCRIPT_DIR, REWRITE_SCRIPT, SUBPROCESS_TIMEOUT, force, mode, source) for pid in pids]

    # 中断标志（threading.Event，信号处理器只 set，主循环检查）
    interrupt_event = threading.Event()
    executor = None  # 提前声明，避免信号处理器中 NameError

    def on_sigint(signum, frame):
        """信号处理器：只设置标志位，不做复杂操作"""
        interrupt_event.set()
        # 恢复默认 SIGINT 处理器，第二次 Ctrl+C 直接退出
        signal.signal(signal.SIGINT, signal.SIG_DFL)

    original_handler = signal.signal(signal.SIGINT, on_sigint)

    executor = ProcessPoolExecutor(max_workers=max_workers)

    try:
        futures = {executor.submit(process_one_pid, task): task[0] for task in tasks}

        for future in as_completed(futures):
            # 检查是否收到中断信号
            if interrupt_event.is_set():
                print(f"\n\n收到 Ctrl+C，正在终止所有子进程...")
                tracker.mark_interrupted()
                _shutdown_executor(executor, wait=False)
                # 取消尚未开始的 future
                for f in futures:
                    f.cancel()
                break

            pid = futures[future]
            try:
                pid_result, status, error = future.result()
                if status == "success":
                    print(f"[完成] {pid}: 成功", flush=True)
                    tracker.mark_success(pid)
                elif status == "waiting":
                    print(f"[完成] {pid}: 等待 Agent 产物", flush=True)
                    tracker.mark_waiting(pid, error or "等待 Agent 写入 03/03.5/04")
                else:
                    print(f"[完成] {pid}: 失败 ({error})", flush=True)
                    tracker.mark_fail(pid, error)
            except Exception as e:
                print(f"[完成] {pid}: 异常 ({e})", flush=True)
                tracker.mark_fail(pid, str(e))

        # 汇总（正常完成或中断都打印）
        summary = tracker.get_summary(max_workers)
        summary_path = SCRIPT_DIR / "log" / "batch_summary.txt"
        summary_path.write_text(summary, encoding="utf-8")
        print(f"\n{summary}")
        print(f"\n汇总已保存到: {summary_path}")

    finally:
        signal.signal(signal.SIGINT, original_handler)
        if executor is not None:
            _shutdown_executor(executor, wait=False)


if __name__ == "__main__":
    # Windows 下 multiprocessing 需要 freeze_support
    multiprocessing.freeze_support()
    main()
