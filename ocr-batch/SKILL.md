---
name: ocr-batch
description: OCR 工具，用于识别图片中的文字内容。支持单图/批量处理、超时控制、多模型切换、自定义 API 地址和 Key。当用户需要提取图片文字、OCR 识别、图片转文字时使用此技能。
license: MIT
---

此技能用于处理图片进行 OCR 文字识别，直接输出到命令行，支持管道组合。

## 使用场景

- 提取图片中的文字内容
- 文档扫描件 OCR 识别
- 截图文字提取
- 图片转文本
- 管道处理（配合 grep、jq 等工具）

## 模型选择指南

| 模型 | 适用场景 | 注意事项 |
|------|----------|----------|
| `ministral-3-4k:latest` | 通用图片理解、图文混合、未知类型 | ✅ 推荐，能处理各种类型图片 |
| `deepseek-ocr:latest` | 纯文档 OCR、扫描件、清晰文字图片 | ⚠️ 非文本图片会无限输出无意义文字 |

**重要**: 对于混合类型或不确定的图片，使用默认的 `ministral-3-4k:latest`。

## CLI 命令

```bash
# 单图处理 - 直接输出文字
python ocr-batch/ocr_batch.py <图片路径>

# 单图处理 - JSON 格式输出
python ocr-batch/ocr_batch.py <图片路径> --json

# 批量处理 - 输出所有图片文字
python ocr-batch/ocr_batch.py <目录路径>

# 批量处理 - JSON 格式输出
python ocr-batch/ocr_batch.py <目录路径> --json

# 使用不同模型
python ocr-batch/ocr_batch.py <图片路径> -m deepseek-ocr:latest

# 自定义超时时间（默认 30 秒）
python ocr-batch/ocr_batch.py <图片路径> -t 60

# 自定义 API 地址
python ocr-batch/ocr_batch.py <图片路径> --api-url http://localhost:11434

# 自定义 API Key
python ocr-batch/ocr_batch.py <图片路径> --api-url http://api.example.com --api-key sk-xxx

# 管道处理
python ocr-batch/ocr_batch.py <图片路径> | grep "关键词"
python ocr-batch/ocr_batch.py <图片路径> --json | jq '.text'
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `source` | 图片文件或目录路径（必需） | - |
| `-m, --model` | OCR 模型 | `ministral-3-4k:latest` |
| `--json` | 输出 JSON 格式 | - |
| `-t, --timeout` | 超时时间 (秒) | `30` |
| `--api-url` | 自定义 API 地址 | 默认本地 ollama |
| `--api-key` | 自定义 API Key (Bearer Token) | - |

## 输出格式

### 文本模式（默认）

单图：
```
识别的文字内容...
```

批量：
```
=== image1.jpg ===
图片 1 的文字内容...

=== image2.jpg ===
图片 2 的文字内容...
```

### JSON 模式（--json）

单图：
```json
{
  "source": "图片路径",
  "model": "使用的模型",
  "text": "识别的文字内容"
}
```

批量：
```json
{
  "results": [
    {
      "source": "图片路径",
      "model": "使用的模型",
      "text": "识别的文字内容",
      "status": "success"
    }
  ],
  "stats": {
    "success": 1,
    "failed": 0,
    "skipped": 0
  }
}
```

## 错误处理

错误信息输出到 stderr，JSON 格式：
```json
{"error": "错误信息", "source": "图片路径"}
```

## 执行步骤

当用户请求 OCR 处理时：

1. 确认图片/目录路径
2. 根据图片类型推荐模型（文档用 deepseek-ocr，其他用 ministral-3-4k）
3. 如有需要，配置自定义 API 地址和 Key
4. 执行 OCR 命令
5. 返回识别结果

## 环境变量（可选）

也可以通过环境变量配置默认 API 地址和 Key：

```bash
export OCR_API_URL="http://localhost:11434"
export OCR_API_KEY="your-api-key"
```

然后在命令中使用：
```bash
python ocr-batch/ocr_batch.py <图片路径> --api-url $OCR_API_URL --api-key $OCR_API_KEY
```