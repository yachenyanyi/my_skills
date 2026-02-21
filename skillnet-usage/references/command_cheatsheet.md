# SkillNet 命令速查表

## 一行命令速查

```bash
# 搜索技能
skillnet search "关键词" [--mode vector] [--limit 10]

# 下载技能
skillnet download <GitHub_URL> [-d 目标目录]

# 创建技能
skillnet create --prompt "描述" [-m gpt-4o]

# 评估技能
skillnet evaluate <路径/URL> [-m gpt-4o]

# 分析关系
skillnet analyze <目录> [--save]
```

---

## 参数对照表

| 命令 | 必需参数 | 常用选项 | 默认值 |
|------|----------|----------|--------|
| search | 关键词 | --mode, --category, --limit | keyword, 20 |
| download | URL | -d, -t | 当前目录 |
| create | 轨迹文件/--prompt/--github/--office | -d, -m, --max-files | gpt-4o |
| evaluate | TARGET | --name, -m | gpt-4o |
| analyze | SKILLS_DIR | --save, -m | save, gpt-4o |

---

## 评估维度评级标准

| 维度 | Good | Average | Poor |
|------|------|---------|------|
| Safety | 安全无破坏 | 无明显 safeguard | 鼓励危险操作 |
| Completeness | 步骤完整清晰 | 部分缺失 | 核心步骤缺失 |
| Executability | 可直接运行 | 需少量调整 | 无法执行 |
| Maintainability | 模块化易改 | 可改但紧耦合 | 难以修改 |
| Cost_awareness | 明确限制 | 无明显浪费 | 鼓励无界消耗 |

---

## 关系类型说明

| 类型 | 方向 | 示例 |
|------|------|------|
| similar_to | 双向 | google_search ↔ bing_search |
| belong_to | 子→父 | 数据清洗 → 数据分析工作流 |
| compose_with | 双向 | PDF 解析 ↔ 文本总结 |
| depend_on | 依赖→前提 | API 客户端 → API 密钥配置 |

---

## 环境变量的设置

```bash
# Linux/Mac
export OPENAI_API_KEY='sk-xxx'
export GITHUB_TOKEN='ghp_xxx'

# Windows (PowerShell)
$env:OPENAI_API_KEY='sk-xxx'
$env:GITHUB_TOKEN='ghp_xxx'

# 写入 .env 文件
echo "OPENAI_API_KEY=sk-xxx" >> .env
```

---

## 常见错误及解决

| 错误 | 原因 | 解决 |
|------|------|------|
| No results found | 关键词太具体 | 换用更通用词或用 vector 模式 |
| Download failed | 网络/GitHub 限流 | 配置 GITHUB_TOKEN |
| API key not configured | 未设置 API Key | export OPENAI_API_KEY |
| LiteLLM not installed | 未安装依赖 | pip install litellm |

---

## 工作流模板

### 查找 + 下载 + 评估
```bash
skillnet search "数据可视化" --limit 5
skillnet download <选中的 URL> -d ./skills
skillnet evaluate ./skills/<技能名>
```

### 创建 + 评估
```bash
skillnet create --prompt "爬虫技能" -d ./skills
skillnet evaluate ./skills/<生成的技能名>
```

### 批量分析
```bash
skillnet analyze ./skills --save
cat relationships.json | jq '.'
```