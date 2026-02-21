---
name: skillnet-usage
description: SkillNet AI 命令行工具完整使用指南。当用户需要了解 SkillNet 平台的技能搜索、下载、创建、评估等功能时调用此技能。提供 5 个核心命令的详细用法、参数说明和实战示例。
---

# SkillNet AI 使用指南

## 概述

SkillNet 是一个 AI 技能平台，可以**创建、下载、评估、搜索** AI 技能包。

**官网**: http://skillnet.openkg.cn

**安装**: `pip install skillnet-ai`

---

## 5 个核心命令

### 1. search - 搜索技能

在 SkillNet 平台上搜索技能，支持关键词匹配和向量语义搜索。

#### 基本用法

```bash
# 关键词搜索（默认）
skillnet search "网页爬虫"

# 向量语义搜索（AI 理解意图）
skillnet search "帮我抓取网页数据" --mode vector

# 带过滤条件
skillnet search "API" --category Development --min-stars 3 --limit 10
```

#### 参数说明

| 参数 | 说明 | 默认值 | 适用模式 |
|------|------|--------|----------|
| `--mode` | `keyword` 或 `vector` | keyword | 通用 |
| `--category` | 分类过滤，如 `Development` | 无 | keyword |
| `--limit` | 返回数量上限 | 20 | 通用 |
| `--page` | 页码 | 1 | keyword |
| `--min-stars` | 最低星级 | 0 | keyword |
| `--sort-by` | `stars` 或 `recent` | stars | keyword |
| `--threshold` | 相似度阈值 0.0-1.0 | 0.8 | vector |

#### 输出示例

```
                       Search Results: 网页搜索 (7 items)
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Name                ┃ Category  ┃ Stars ┃ Descript… ┃ Evaluati… ┃ URL        ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ multi-search-engine │ Research  │  1097 │ 集成 7 大 … │ Safety:   │ https://gi │
│                     │           │       │ when user │ Good      │ thub.com/o │
│                     │           │       │ needs to  │ Cxecutab… │ penclaw/sk │
│                     │           │       │ search    │ Good      │ ills/blob/ │
│                     │           │       │ informat… │ Good      │ e33b5f261b │
│                     │           │       │ online,   │ Maintain… │ bd8b5e4747 │
│                     │           │       │ compare   │ Good      │ 7209748a80 │
│                     │           │       │ se...     │ Cost-Awa… │ 91e219252a │
│                     │           │       │           │ Average   │ 91e219252a │
└─────────────────────┴───────────┴───────┴───────────┴───────────┴────────────┘

Tip: Use 'skillnet download <skill_url>' to get a skill.
```

---

### 2. download - 下载技能

从 GitHub 下载并安装技能到本地。

#### 基本用法

```bash
# 下载技能到当前目录
skillnet download https://github.com/owner/repo/tree/main/skills/math_solver

# 指定安装目录
skillnet download https://github.com/.../skill -d ./my_skills

# 使用 GitHub Token（私有仓库或提高限流）
skillnet download https://github.com/.../skill -t ghp_xxx
```

#### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `URL` | GitHub 技能文件夹链接（必需） | - |
| `-d, --target-dir` | 安装目录 | 当前目录 |
| `-t, --token` | GitHub Token | 环境变量 `GITHUB_TOKEN` |

#### 安装成功输出

```
Target directory: /path/to/install
                   Installation Successful
 Skill:     skill-name
 Location:  /path/to/install/skill-name

✅ skill-name is ready to use.
```

---

### 3. create - 用 AI 创建技能

从轨迹文件、GitHub 仓库、办公文档或提示词创建技能包。

#### 基本用法

```bash
# 从轨迹文件创建
skillnet create trajectory.txt

# 从 GitHub 仓库创建
skillnet create --github https://github.com/owner/repo

# 从办公文档创建（PDF/Word/PPT）
skillnet create --office document.pdf

# 直接用提示词创建
skillnet create --prompt "创建一个抓取微信公众号文章的技能"

# 指定输出目录和模型
skillnet create --prompt "数据分析技能" -d ./output -m gpt-4o
```

#### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `TRAJECTORY_FILE` | 操作轨迹/日志文件路径 | - |
| `-g, --github` | GitHub 仓库 URL | - |
| `-o, --office` | 办公文档路径（PDF/PPT/Word） | - |
| `-p, --prompt` | 直接描述技能需求 | - |
| `-d, --output-dir` | 输出目录 | `generated_skills` |
| `-m, --model` | LLM 模型 | `gpt-4o` |
| `--max-files` | 最大分析文件数（仅 github） | 20 |

#### 输出格式

```
## FILE: skill-name/SKILL.md
```yaml
---
name: skill-name
description: 当用户需要...时使用此技能
---
# 技能说明
...
```

## FILE: skill-name/scripts/main.py
```python
# 脚本代码
...
```
```

---

### 4. evaluate - 评估技能质量

使用 AI 评估技能的安全性、完整性、可执行性等维度。

#### 基本用法

```bash
# 评估本地技能
skillnet evaluate ./my_skill

# 评估 GitHub 上的技能
skillnet evaluate https://github.com/user/repo/tree/main/skill

# 指定描述信息
skillnet evaluate ./skill --name "数据爬虫" --description "抓取网页数据"

# 使用指定模型
skillnet evaluate ./skill -m gpt-4o
```

#### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `TARGET` | 本地路径或 GitHub URL（必需） | - |
| `--name` | 技能名称 | 自动检测 |
| `--category` | 分类 | 自动检测 |
| `--description` | 简短描述 | 自动检测 |
| `-m, --model` | LLM 模型 | `gpt-4o` |
| `--max-workers` | 并发数（批量评估） | 5 |

#### 评估维度

| 维度 | 评估内容 | 评级 |
|------|----------|------|
| **Safety** | 潜在危害/滥用风险 | Good/Average/Poor |
| **Completeness** | 步骤/约束是否完整 | Good/Average/Poor |
| **Executability** | 能否实际执行 | Good/Average/Poor |
| **Maintainability** | 可复用/组合性 | Good/Average/Poor |
| **Cost_awareness** | 时间/算力/金钱意识 | Good/Average/Poor |

#### 输出示例

```json
{
  "safety": {
    "level": "Good",
    "reason": "技能操作安全，无破坏性行为，有明确错误处理"
  },
  "completeness": {
    "level": "Average",
    "reason": "主要步骤清晰，但缺少输入验证和边界条件说明"
  },
  "executability": {
    "level": "Good",
    "reason": "提供了完整代码示例和依赖说明，可直接运行"
  },
  "maintainability": {
    "level": "Good",
    "reason": "模块化设计，配置与代码分离，易于修改"
  },
  "cost_awareness": {
    "level": "Average",
    "reason": "未提及调用限制和成本优化建议"
  }
}
```

---

### 5. analyze - 分析技能关系

分析本地技能之间的逻辑关系，构建知识图谱。

#### 基本用法

```bash
# 分析技能目录
skillnet analyze ./skills_folder

# 保存结果到 JSON
skillnet analyze ./skills_folder --save

# 使用指定模型
skillnet analyze ./skills_folder -m gpt-4o
```

#### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `SKILLS_DIR` | 包含多个技能的目录（必需） | - |
| `--save` / `--no-save` | 是否保存到 `relationships.json` | save |
| `-m, --model` | LLM 模型 | `gpt-4o` |

#### 关系类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `similar_to` | 功能等价，可互换 | google_search ↔ bing_search |
| `belong_to` | 子组件属于大流程 | 数据清洗 ↔ 数据分析工作流 |
| `compose_with` | 独立但常配合使用 | PDF 解析 ↔ 文本总结 |
| `depend_on` | 硬依赖，无此不可运行 | API 客户端 ↔ API 密钥配置 |

#### 输出示例

```json
[
  {
    "source": "pdf_parser",
    "target": "text_summarizer",
    "type": "compose_with",
    "reason": "PDF 解析后通常需要文本总结，两者常配合使用"
  },
  {
    "source": "web_scraper",
    "target": "data_cleaner",
    "type": "compose_with",
    "reason": "网页抓取的数据通常需要清洗处理"
  }
]
```

---

## 实战工作流

### 工作流 1：查找并安装现成技能

```bash
# 1. 搜索技能
skillnet search "数据可视化" --limit 10

# 2. 查看评价，选择高星技能

# 3. 下载技能
skillnet download https://github.com/.../chart-generator

# 4. 按提示配置依赖
```

### 工作流 2：从 GitHub 仓库创建技能

```bash
# 1. 从仓库创建
skillnet create --github https://github.com/user/repo -d ./skills

# 2. 查看生成的技能

# 3. 评估技能质量
skillnet evaluate ./skills/repo-name

# 4. 根据评估反馈优化
```

### 工作流 3：从文档创建技能

```bash
# 1. 从 PDF 创建
skillnet create --office manual.pdf -d ./skills

# 2. 从 PPT 创建
skillnet create --office training.pptx -d ./skills

# 3. 从 Word 创建
skillnet create --office guide.docx -d ./skills
```

### 工作流 4：批量评估技能库

```bash
# 准备 JSONL 文件
cat > skills.jsonl << EOF
{"skill_url": "https://github.com/.../skill1"}
{"skill_url": "https://github.com/.../skill2"}
{"skill_path": "./local_skill1"}
EOF

# 批量评估
skillnet evaluate --input skills.jsonl --output results.jsonl
```

---

## 环境配置

### API Key 配置

`create`、`evaluate`、`analyze` 命令需要 LLM API Key。

```bash
# 方式 1：环境变量
export OPENAI_API_KEY='sk-xxx'
export BASE_URL='https://api.openai.com/v1'  # 可选，兼容地址

# 方式 2：使用 .env 文件
echo "OPENAI_API_KEY=sk-xxx" > .env
```

### GitHub Token 配置

下载私有仓库或提高 API 限流。

```bash
# 方式 1：命令行参数
skillnet download <url> -t ghp_xxx

# 方式 2：环境变量
export GITHUB_TOKEN='ghp_xxx'
```

---

## 常见问题

### Q: search 命令返回结果为空？

A: 尝试以下方法：
- 换用更通用的关键词
- 使用 `--mode vector` 语义搜索
- 放宽 `--min-stars` 限制

### Q: download 命令失败？

A: 检查：
- GitHub 链接是否为 `/tree/` 格式
- 网络是否可访问 GitHub
- 是否需要配置 `GITHUB_TOKEN`

### Q: create 命令很慢？

A: 分析大量文件时正常，可：
- 使用 `--max-files` 限制分析数量
- 使用更快的模型如 `gpt-3.5-turbo`

### Q: evaluate 结果不准确？

A: 尝试：
- 提供更详细的 `--name`、`--description`
- 使用更强的模型如 `gpt-4o`
- 检查技能的 `SKILL.md` 是否完整

---

## 依赖说明

| 依赖 | 用途 | 必需场景 |
|------|------|----------|
| `openai` | LLM 调用 | create/evaluate/analyze |
| `pycryptodome` | 加密解密 | 部分技能需要 |
| `PyPDF2` | PDF 读取 | create --office PDF |
| `python-docx` | Word 读取 | create --office Word |
| `python-pptx` | PPT 读取 | create --office PPT |
| `requests` | HTTP 请求 | download/search |
| `typer` | CLI 框架 | 全部命令 |
| `rich` | 美化输出 | 全部命令 |

---

## 最佳实践

1. **搜索时先用 keyword，再用 vector** - keyword 快速浏览，vector 深度匹配
2. **下载前检查评价** - Safety/Executability 为 Poor 的技能慎用
3. **创建后务必评估** - 确保生成的技能质量过关
4. **定期分析技能关系** - 发现冗余技能，优化技能库
5. **保存评估结果** - 建立技能质量档案，便于团队共享

---

## 资源

- **官网**: http://skillnet.openkg.cn
- **GitHub**: https://github.com/skillnet-ai/skillnet-ai
- **文档**: `skillnet --help`
- **技能市场**: https://github.com/topics/skillnet