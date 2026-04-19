# VitePress 博客管理器

一个用Python开发的CLI工具，方便您快速创建、管理、预览和发布VitePress博客。

## 功能特性

? **主要功能**：
- ? 快速创建新文章（自动生成Markdown模板）
- ? 列出和管理所有文章
- ? 快速打开文章进行编辑
- ?? 本地预览开发服务器
- ? 构建静态站点
- ? 一键提交并推送到GitHub
- ? 查看博客统计信息

## 安装

### 前置要求

- Python 3.7+
- Node.js 和 npm（用于VitePress）
- Git（用于提交和推送）

### 设置步骤

1. 确保在项目根目录中：
```bash
cd /path/to/Aron.Zhou.github.io
```

2. 将 `blog_manager.py` 放在项目根目录

3. 给脚本添加执行权限（Linux/macOS）：
```bash
chmod +x blog_manager.py
```

## 使用方法

### 1. 创建新文章

**创建在根目录：**
```bash
python blog_manager.py create "我的第一篇文章"
```

**创建在特定分类：**
```bash
python blog_manager.py create "BLE协议分析" --category ble --description "深入理解BLE协议"
```

这会在 `docs/ble/` 目录创建一个文章，带有现成的Markdown模板。

### 2. 列出所有文章

**列出所有文章：**
```bash
python blog_manager.py list
```

**只列出某个分类的文章：**
```bash
python blog_manager.py list --category ble
```

输出示例：
```
? ble/ananlyzer.md
? markdown-examples.md
? api-examples.md

共找到 3 篇文章
```

### 3. 打开文章编辑

```bash
python blog_manager.py open ble/ananlyzer.md
```

或者只需输入文件名片段：
```bash
python blog_manager.py open ananlyzer
```

脚本会自动在您的默认编辑器中打开文件。

### 4. 本地预览

启动开发服务器在 `http://localhost:5173`：
```bash
python blog_manager.py preview
```

按 `Ctrl+C` 停止服务器。

### 5. 构建站点

生成静态文件到 `dist/` 目录：
```bash
python blog_manager.py build
```

### 6. 发布到GitHub

构建并提交所有更改：
```bash
python blog_manager.py publish --message "Add new article about BLE"
```

或使用默认提交消息：
```bash
python blog_manager.py publish
```

这个命令会：
1. 执行 `git add .`
2. 用提交消息执行 `git commit`
3. 执行 `git push`

### 7. 查看博客统计

```bash
python blog_manager.py stats
```

输出示例：
```
? 博客统计信息
  ? 文章总数: 3
  ? 总字数: 5,432
  ? 平均字数: 1,810
```

## 完整的工作流示例

```bash
# 1. 创建新文章
python blog_manager.py create "Python最佳实践" --category tutorials --description "分享Python编程的最佳实践"

# 2. 打开文章编辑（在您的编辑器中编辑内容）
python blog_manager.py open tutorials/python-best-practices.md

# 3. 本地预览效果
python blog_manager.py preview
# 访问 http://localhost:5173 查看效果

# 4. 构建站点
python blog_manager.py build

# 5. 发布到GitHub
python blog_manager.py publish --message "Add Python best practices guide"

# 6. 查看统计
python blog_manager.py stats
```

## 文件结构

```
Aron.Zhou.github.io/
├── blog_manager.py          # 本工具
├── docs/
│   ├── index.md
│   ├── markdown-examples.md
│   ├── api-examples.md
│   ├── ble/
│   │   └── ananlyzer.md
│   └── .vitepress/
│       └── config.mts
├── package.json
└── .git/
```

## 创建的Markdown模板

当您创建新文章时，会自动生成以下模板：

```markdown
# 文章标题

> 文章描述

**发布时间**: 2024-XX-XX

## 概述

在这里介绍您的文章内容...

## 主要内容

### 第一节

您的内容...

### 第二节

您的内容...

## 总结

总结要点...

## 参考资源

- [参考链接1](#)
- [参考链接2](#)
```

您可以直接在这个基础上编辑内容。

## 故障排除

### 问题：找不到npm命令
**解决方案**：确保已安装Node.js和npm，且在系统PATH中。

### 问题：预览服务器无法启动
**解决方案**：检查是否已安装VitePress依赖：
```bash
npm install
```

### 问题：Git提交失败
**解决方案**：
1. 确保已初始化Git仓库：`git init`
2. 配置Git用户名和邮箱：
```bash
git config user.name "Your Name"
git config user.email "your@email.com"
```

## 进阶用法

### 为特定分类创建多个文章

```bash
# 创建BLE系列文章
python blog_manager.py create "BLE介绍" --category ble
python blog_manager.py create "BLE通信协议" --category ble
python blog_manager.py create "BLE应用开发" --category ble

# 列出所有BLE文章
python blog_manager.py list --category ble
```

### 自定义工作流脚本

在项目根目录创建 `publish.sh`（Linux/macOS）或 `publish.bat`（Windows）：

**publish.sh:**
```bash
#!/bin/bash
echo "? 构建中..."
python blog_manager.py build

echo "? 发布中..."
python blog_manager.py publish --message "$1"

echo "? 完成!"
```

使用方法：
```bash
./publish.sh "New article about BLE"
```

## 技术细节

- **语言**：Python 3.7+
- **依赖**：标准库（无需额外安装）
- **跨平台**：支持 Windows, macOS, Linux

## 扩展建议

您可以扩展此工具，添加以下功能：

1. **图片管理** - 自动处理和优化博客图片
2. **搜索索引** - 生成搜索索引文件
3. **SEO优化** - 自动生成元数据
4. **分析集成** - 集成分析工具
5. **评论系统** - 集成评论功能
6. **备份** - 自动备份博客内容
7. **模板管理** - 支持自定义文章模板

## 许可证

ISC License

## 联系和反馈

如有问题或建议，请通过GitHub提交Issue。

---

**祝您博客写作愉快！** ??
