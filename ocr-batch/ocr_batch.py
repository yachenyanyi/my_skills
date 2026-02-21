#!/usr/bin/env python3
"""
OCR 工具 - 直接输出到命令行
适用于单图和批量处理，支持管道组合

支持自定义模型、API 地址和 API Key
"""

import json
import sys
import time
import threading
import os
from pathlib import Path
from typing import Optional

try:
    import ollama
except ImportError:
    print(json.dumps({"error": "请安装 ollama: pip install ollama"}), file=sys.stderr)
    sys.exit(1)


class OCRProcessor:
    def __init__(
        self,
        model: str = "ministral-3-4k:latest",
        retry_count: int = 3,
        retry_delay: float = 2.0,
        timeout: float = 30.0,
        api_url: str = None,
        api_key: str = None,
    ):
        self.model = model
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.timeout = timeout
        self.api_url = api_url
        self.api_key = api_key
        self.extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff'}

    def _get_image_files(self, source: Path) -> list[Path]:
        if source.is_file():
            if source.suffix.lower() in self.extensions:
                return [source]
            return []

        files = []
        for ext in self.extensions:
            files.extend(source.glob(f"*{ext}"))
            files.extend(source.glob(f"*{ext.upper()}"))
        return sorted(files)

    def _get_client(self):
        """获取 ollama 客户端，支持自定义 API 地址和 Key"""
        if self.api_url:
            # 自定义 API 地址
            headers = {}
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'
            return ollama.Client(host=self.api_url, headers=headers) if headers else ollama.Client(host=self.api_url)
        return None

    def _ocr_single(self, image_path: Path) -> Optional[str]:
        result_container = {"result": None, "error": None}

        def _call_ollama():
            try:
                client = self._get_client()
                if client:
                    # 使用自定义客户端
                    response = client.chat(
                        model=self.model,
                        messages=[{
                            'role': 'user',
                            'content': 'Free OCR',
                            'images': [str(image_path)]
                        }]
                    )
                else:
                    # 使用默认配置
                    response = ollama.chat(
                        model=self.model,
                        messages=[{
                            'role': 'user',
                            'content': 'Free OCR',
                            'images': [str(image_path)]
                        }]
                    )
                result_container["result"] = response['message']['content']
            except Exception as e:
                result_container["error"] = e

        for attempt in range(self.retry_count):
            result_container = {"result": None, "error": None}

            thread = threading.Thread(target=_call_ollama, daemon=True)
            thread.start()
            thread.join(timeout=self.timeout)

            if thread.is_alive():
                raise TimeoutError(f"OCR 处理超时 (>{self.timeout}秒)")

            if result_container["error"]:
                if attempt < self.retry_count - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                else:
                    raise result_container["error"]

            if result_container["result"]:
                return result_container["result"]

        return None

    def process_single(self, image_path: Path, output_format: str = "text") -> bool:
        try:
            result = self._ocr_single(image_path)
            if result:
                if output_format == "json":
                    data = {
                        "source": str(image_path),
                        "model": self.model,
                        "text": result
                    }
                    print(json.dumps(data, ensure_ascii=False))
                else:
                    print(result)
                return True
            else:
                print(json.dumps({"error": "OCR 返回空结果", "source": str(image_path)}), file=sys.stderr)
                return False
        except Exception as e:
            print(json.dumps({"error": str(e), "source": str(image_path)}), file=sys.stderr)
            return False

    def process_batch(self, source: str, output_format: str = "text") -> dict:
        source_path = Path(source)
        if not source_path.exists():
            print(json.dumps({"error": f"路径不存在：{source}"}), file=sys.stderr)
            return {"success": 0, "failed": 0, "skipped": 0}

        images = self._get_image_files(source_path)
        if not images:
            print(json.dumps({"error": f"未找到图片文件：{source}"}), file=sys.stderr)
            return {"success": 0, "failed": 0, "skipped": 0}

        stats = {"success": 0, "failed": 0, "skipped": 0}
        results = []

        for i, img in enumerate(images, 1):
            try:
                result = self._ocr_single(img)
                if result:
                    if output_format == "json":
                        results.append({
                            "source": str(img),
                            "model": self.model,
                            "text": result,
                            "status": "success"
                        })
                    else:
                        print(f"=== {img.name} ===")
                        print(result)
                        print()
                    stats["success"] += 1
                else:
                    stats["failed"] += 1
            except Exception as e:
                stats["failed"] += 1
                print(json.dumps({"error": str(e), "source": str(img)}), file=sys.stderr)

        if output_format == "json":
            print(json.dumps({
                "results": results,
                "stats": stats
            }, ensure_ascii=False))

        return stats


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="OCR 工具 - 直接输出到命令行",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 单图处理
  %(prog)s image.jpg
  %(prog)s image.jpg --json

  # 批量处理
  %(prog)s ./images/
  %(prog)s ./images/ --json

  # 管道处理
  %(prog)s image.jpg | grep "关键词"
  %(prog)s image.jpg --json | jq '.text'

  # 使用不同模型
  %(prog)s image.jpg -m deepseek-ocr:latest

  # 自定义 API 地址
  %(prog)s image.jpg --api-url http://localhost:11434

  # 自定义 API Key
  %(prog)s image.jpg --api-url http://api.example.com --api-key sk-xxx

  # 完整配置
  %(prog)s image.jpg -m ministral-3-4k -t 60 --api-url http://localhost:11434 --api-key your-key
        """
    )

    parser.add_argument("source", help="图片文件或目录路径")
    parser.add_argument("-m", "--model", default=None, help="OCR 模型 (默认：ministral-3-4k:latest)")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("-t", "--timeout", type=float, default=30.0, help="超时时间 (秒) (默认：30)")
    parser.add_argument("--api-url", default=None, help="自定义 API 地址 (如：http://localhost:11434)")
    parser.add_argument("--api-key", default=None, help="自定义 API Key (Bearer Token)")

    args = parser.parse_args()

    # 如果未指定模型，使用默认值
    model = args.model if args.model else "ministral-3-4k:latest"

    processor = OCRProcessor(
        model=model,
        timeout=args.timeout,
        api_url=args.api_url,
        api_key=args.api_key,
    )

    source_path = Path(args.source)
    output_format = "json" if args.json else "text"

    if source_path.is_file():
        success = processor.process_single(source_path, output_format)
        sys.exit(0 if success else 1)
    else:
        processor.process_batch(args.source, output_format)


if __name__ == "__main__":
    main()