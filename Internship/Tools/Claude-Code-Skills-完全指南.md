# Claude Code Skills 完全指南

> 适用版本: Claude Code CLI (2026-07)
> 本文档基于当前环境实际安装的 Skills 编写

---

## 目录

1. [什么是 Skill](#1-什么是-skill)
2. [Skill 的存储架构](#2-skill-的存储架构)
3. [如何安装 Skill](#3-如何安装-skill)
4. [如何卸载 Skill](#4-如何卸载-skill)
5. [如何创建自定义 Skill](#5-如何创建自定义-skill)
6. [如何使用 Skill](#6-如何使用-skill)

---

## 1. 什么是 Skill

Skill 是 Claude Code 的**可复用能力模块**。每个 Skill 是一份 Markdown 文档（`SKILL.md`），包含特定领域的知识、流程规范、最佳实践。当你的任务匹配某个 Skill 的触发条件时，Claude Code 会自动加载该 Skill 的指令来指导行为。

**Skill 的本质**: 一套写给 AI 看的"标准作业程序"(SOP)，确保 Claude 在特定场景下表现一致、专业。

**Skill vs Hook vs Plugin**:

| 概念 | 作用 | 存储位置 |
|------|------|----------|
| **Skill** | 知识/流程指导文档 | `~/.claude/skills/` 或插件内 |
| **Command** | 用户可手动调用的快捷命令 | `~/.claude/commands/` |
| **Hook** | 事件触发的自动化脚本 | `settings.json` 中配置 |
| **Plugin** | Skill + Command + Hook 的打包分发形式 | `~/.claude/plugins/` |

---

## 2. Skill 的存储架构

Skills 按来源分三层存储：

```
~/.claude/
├── commands/                    # 用户级 Commands（可手动调用）
│   └── xxx.md                   # 带 user-invocable: true 的 skill
│
├── skills/                      # 本地 Skills（Git 管理）
│   └── dot-skill/               # 示例：dot-skill 自我蒸馏工具
│       └── SKILL.md
│
├── plugins/
│   ├── marketplaces/            # 插件市场源文件（只读缓存）
│   │   ├── anthropic-agent-skills/skills/   # document-skills
│   │   ├── claude-plugins-official/         # vercel + 官方工具
│   │   └── superpowers-marketplace/         # (源)
│   │
│   └── cache/                   # 插件运行时缓存
│       ├── anthropic-agent-skills/document-skills/
│       ├── claude-plugins-official/vercel/
│       └── superpowers-marketplace/superpowers/
│
└── settings.json                # enabledPlugins 控制启用哪些插件
```

### 当前启用的插件（settings.json）

```json
"enabledPlugins": {
    "superpowers@superpowers-marketplace": true,
    "document-skills@anthropic-agent-skills": true,
    "vercel@claude-plugins-official": true
}
```

每个插件贡献一组 Skills：

| 插件 | 来源 | Skills 数量 | 典型 Skill |
|------|------|-------------|------------|
| `superpowers` | github.com/obra/superpowers-marketplace | ~15 | brainstorming, TDD, debugging |
| `document-skills` | github.com/anthropics/skills | ~18 | pdf, xlsx, pptx, frontend-design |
| `vercel` | Vercel 官方 | ~30+ | deploy, ai-sdk, nextjs, firewall |

---

## 3. 如何安装 Skill

### 方式 A：通过插件市场安装（推荐）

```bash
# 安装整个插件（包含一组 Skills）
claude plugins install <plugin-name>@<marketplace>

# 示例
claude plugins install vercel@claude-plugins-official
claude plugins install document-skills@anthropic-agent-skills
claude plugins install superpowers@superpowers-marketplace
```

**添加第三方市场**（如果市场不在官方列表中）:

在 `settings.json` 的 `extraKnownMarketplaces` 中添加:

```json
"extraKnownMarketplaces": {
    "superpowers-marketplace": {
        "source": {
            "source": "github",
            "repo": "obra/superpowers-marketplace"
        }
    }
}
```

### 方式 B：手动创建本地 Skill

在 `~/.claude/skills/<skill-name>/` 下创建 `SKILL.md`:

```markdown
---
name: my-skill
description: Use when [触发条件]
---

# My Skill

## Overview
...
```

### 方式 C：通过 dot-skill 蒸馏生成

使用 `dot-skill` skill 可以从聊天记录中提取人物/角色特征，生成一个 Command 文件到 `~/.claude/commands/`。

### 方式 D：安装单个 Skill（从 Anthropic Skills 仓库）

```bash
# 克隆官方 skills 仓库
git clone https://github.com/anthropics/skills.git

# 复制需要的 skill 到本地
cp -r skills/pdf ~/.claude/skills/pdf
```

---

## 4. 如何卸载 Skill

卸载方式取决于安装方式：

### 卸载整个插件

```bash
# 查看已安装插件
claude plugins list

# 卸载插件（同时移除其所有 Skills）
claude plugins uninstall <plugin-name>

# 示例：卸载 vercel 插件
claude plugins uninstall vercel
```

### 卸载单个本地 Skill

```bash
# 删除对应的 skill 目录
rm -rf ~/.claude/skills/<skill-name>
```

### 卸载单个 Command

```bash
# 删除对应的 .md 文件
rm ~/.claude/commands/<command-name>.md
```

### 禁用插件而不卸载

在 `settings.json` 中将对应插件设为 `false`:

```json
"enabledPlugins": {
    "vercel@claude-plugins-official": false   // 禁用但保留
}
```

---

## 5. 如何创建自定义 Skill

### 目录结构

```
~/.claude/skills/<skill-name>/
├── SKILL.md          # 主文件（必需）
└── helpers.py        # 辅助脚本（可选）
```

### SKILL.md 模板

```markdown
---
name: my-skill-name
description: Use when [具体触发条件] - 用 "Use when..." 开头,只写触发条件不写流程
---

# Skill Name

## Overview
一句话说清这是什么，核心原则是什么。

## When to Use
- 场景 A 的症状
- 场景 B 的症状
- 明确不适用于什么情况

## Core Pattern
核心流程/模式说明（代码示例、流程图等）

## Quick Reference
| 操作 | 命令/方法 |
|------|-----------|
| ...  | ...       |

## Common Mistakes
- 错误做法 → 正确做法
```

### Skill 类型

| 类型 | 用途 | 例子 |
|------|------|------|
| **Technique** | 具体操作步骤 | condition-based-waiting |
| **Pattern** | 思考方式/心智模型 | flatten-with-flags |
| **Reference** | API 文档/语法参考 | pdf, xlsx, pptx |
| **Discipline** | 规则约束（防偷懒） | TDD, verification-before-completion |

### 关键规则

1. **描述字段只写触发条件，不写流程** — 否则 Agent 会只看描述跳过正文
2. **命名用字母、数字、连字符** — 不用括号和特殊字符
3. **一个优秀的示例胜过五个平庸的**

---

## 6. 如何使用 Skill

### 自动触发

大多数 Skill 不需要手动调用。当你的任务匹配 Skill 的 `description` 触发条件时，Claude Code 自动加载。例如：

- 你说 "部署到 Vercel" → 自动触发 `vercel:deploy`
- 你说 "帮我写个 PDF" → 自动触发 `document-skills:pdf`
- 你说 "有个 bug 帮我看看" → 自动触发 `superpowers:systematic-debugging`

### 手动调用

部分 Skill 标记了 `user-invocable: true`，可以用斜杠命令手动调用：

```
/superpowers:brainstorming
/vercel:deploy prod
```

### Skill 优先级

当多个 Skill 同时匹配时，**流程类 Skill 优先于执行类 Skill**：

1. 先跑 brainstorming（明确需求）
2. 再跑 implementation（具体实施）
3. 最后跑 verification（验证结果）
