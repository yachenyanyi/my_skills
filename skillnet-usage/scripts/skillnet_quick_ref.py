#!/usr/bin/env python3
"""
SkillNet 快速参考脚本

用法:
    python skillnet_quick_ref.py
"""

COMMANDS = {
    "search": {
        "desc": "搜索技能",
        "usage": 'skillnet search "关键词" [选项]',
        "examples": [
            'skillnet search "网页爬虫"',
            'skillnet search "API" --category Development --limit 10',
            'skillnet search "帮我抓取数据" --mode vector',
        ],
        "key_params": {
            "--mode": "keyword (默认) 或 vector",
            "--category": "分类过滤",
            "--limit": "返回数量 (默认 20)",
            "--min-stars": "最低星级",
            "--threshold": "相似度阈值 0-1(仅 vector)",
        }
    },
    "download": {
        "desc": "下载技能",
        "usage": "skillnet download <GitHub_URL> [选项]",
        "examples": [
            "skillnet download https://github.com/.../skill",
            "skillnet download <url> -d ./my_skills",
            "skillnet download <url> -t ghp_xxx",
        ],
        "key_params": {
            "URL": "GitHub 技能文件夹链接",
            "-d": "安装目录",
            "-t": "GitHub Token",
        }
    },
    "create": {
        "desc": "创建技能",
        "usage": "skillnet create [文件] [选项]",
        "examples": [
            "skillnet create trajectory.txt",
            "skillnet create --github https://github.com/owner/repo",
            "skillnet create --office document.pdf",
            'skillnet create --prompt "创建爬虫技能"',
        ],
        "key_params": {
            "TRAJECTORY_FILE": "轨迹文件",
            "--github": "GitHub 仓库 URL",
            "--office": "办公文档路径",
            "--prompt": "直接描述",
            "--model": "LLM 模型 (默认 gpt-4o)",
        }
    },
    "evaluate": {
        "desc": "评估技能",
        "usage": "skillnet evaluate <本地路径/GitHub_URL> [选项]",
        "examples": [
            "skillnet evaluate ./my_skill",
            "skillnet evaluate https://github.com/.../skill",
            "skillnet evaluate ./skill --name 爬虫",
        ],
        "key_params": {
            "TARGET": "本地路径或 GitHub URL",
            "--name": "技能名称",
            "--model": "LLM 模型 (默认 gpt-4o)",
        },
        "dimensions": ["Safety", "Completeness", "Executability", "Maintainability", "Cost_awareness"]
    },
    "analyze": {
        "desc": "分析技能关系",
        "usage": "skillnet analyze <技能目录> [选项]",
        "examples": [
            "skillnet analyze ./skills",
            "skillnet analyze ./skills --save",
        ],
        "key_params": {
            "SKILLS_DIR": "包含多个技能的目录",
            "--save": "保存到 relationships.json",
            "--model": "LLM 模型 (默认 gpt-4o)",
        },
        "relations": ["similar_to", "belong_to", "compose_with", "depend_on"]
    }
}

def print_quick_ref():
    print("=" * 80)
    print("SkillNet AI 快速参考卡片")
    print("=" * 80)
    print()

    for cmd, info in COMMANDS.items():
        print(f"## {cmd.upper()} - {info['desc']}")
        print(f"用法：{info['usage']}")
        print()
        print("示例:")
        for ex in info['examples']:
            print(f"  $ {ex}")
        print()
        print("参数:")
        for param, desc in info['key_params'].items():
            print(f"  {param}: {desc}")

        if 'dimensions' in info:
            print(f"评估维度：{', '.join(info['dimensions'])}")
        if 'relations' in info:
            print(f"关系类型：{', '.join(info['relations'])}")
        print()
        print("-" * 80)
        print()

if __name__ == "__main__":
    print_quick_ref()