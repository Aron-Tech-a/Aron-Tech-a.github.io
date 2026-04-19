# ? 快速开始指南

## 5分钟快速上手

### 第一步：验证环境

确保已安装 Python 3.7+：
```bash
python --version
```

### 第二步：创建您的第一篇文章

打开命令行，进入项目目录：

**Windows:**
```bash
cd E:\Aron.Zhou.github.io
blog create "我的第一篇文章"
```

**Linux/macOS:**
```bash
cd ~/projects/Aron.Zhou.github.io
chmod +x blog.sh
./blog.sh create "我的第一篇文章"
```

或直接使用Python：
```bash
python blog_manager.py create "我的第一篇文章"
```

? 成功！文章已创建在 `docs/` 目录。

### 第三步：编辑文章

打开生成的Markdown文件并编辑内容：
```bash
blog open "我的第一篇文章"
```

### 第四步：本地预览

启动开发服务器查看效果：
```bash
blog preview
```

访问 http://localhost:5173 查看您的博客。

### 第五步：发布

构建并推送到GitHub：
```bash
blog build
blog publish --message "Add my first article"
```

完成！?

---

## 常见任务

### 创建BLE相关文章
```bash
blog create "BLE通信协议" --category ble --description "深入理解BLE"
```

### 查看所有文章
```bash
blog list
```

### 查看BLE分类的文章
```bash
blog list --category ble
```

### 查看博客统计
```bash
blog stats
```

### 一键部署
```bash
blog build && blog publish --message "Update blog"
```

---

## 命令速查表

| 命令 | 说明 | 示例 |
|------|------|------|
| `blog create` | 创建新文章 | `blog create "标题" --category ble` |
| `blog list` | 列出文章 | `blog list` 或 `blog list --category ble` |
| `blog open` | 打开编辑 | `blog open ble/ananlyzer.md` |
| `blog preview` | 本地预览 | `blog preview` |
| `blog build` | 构建站点 | `blog build` |
| `blog publish` | 发布代码 | `blog publish --message "New post"` |
| `blog stats` | 统计信息 | `blog stats` |

---

## 完整工作流示例

```bash
# 1. 创建新的教程系列文章
blog create "Python Web开发入门" --category tutorials

# 2. 打开编辑
blog open python-web-development

# 3. 在编辑器中完成编辑...
# （编辑 docs/tutorials/python-web-development.md）

# 4. 本地预览效果
blog preview
# 在浏览器访问 http://localhost:5173

# 5. 查看所有文章
blog list

# 6. 查看统计
blog stats

# 7. 停止预览 (Ctrl+C)

# 8. 构建产品版本
blog build

# 9. 提交并推送
blog publish --message "Add Python web development tutorial"

# 10. 完成！检查GitHub Pages看效果
```

---

## 文件组织最佳实践

建议按分类组织文章：

```
docs/
├── index.md                    # 首页
├── ble/
│   ├── analyzer.md             # BLE分析器
│   ├── protocol.md             # BLE协议
│   └── applications.md         # BLE应用
├── tutorials/
│   ├── python-basics.md        # Python基础
│   ├── web-development.md      # Web开发
│   └── git-guide.md            # Git教程
└── examples/
    ├── hello-world.md
    └── advanced-patterns.md
```

创建文章时使用分类：
```bash
blog create "BLE协议详解" --category ble
blog create "Python入门" --category tutorials
blog create "Hello World" --category examples
```

---

## 提示和技巧

### ? 快速发布流程
```bash
blog build && blog publish --message "Auto update"
```

### ? 批量创建文章
```bash
blog create "Article 1" --category tutorials
blog create "Article 2" --category tutorials
blog create "Article 3" --category tutorials
```

### ? 查看特定分类
```bash
blog list --category ble
```

### ? 获取完整帮助
```bash
python blog_manager.py -h
```

---

## 遇到问题？

### npm: 未找到命令
→ 安装Node.js: https://nodejs.org/

### git: 未找到命令
→ 安装Git: https://git-scm.com/

### Python: 未找到命令
→ 安装Python: https://www.python.org/

### VitePress依赖缺失
→ 运行: `npm install`

---

## 下一步

- ? 阅读完整文档：[BLOG_MANAGER_README.md](BLOG_MANAGER_README.md)
- ?? 自定义配置：编辑 [blog_config.json](blog_config.json)
- ? 自定义VitePress主题：编辑 `.vitepress/config.mts`
- ? 设置自动部署：配置GitHub Actions

---

祝您写博客愉快！如有问题，欢迎提交Issue。??
