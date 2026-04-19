# ? 启动 GUI 界面

完整的图形用户界面版本，无需命令行，一切都在窗口中点击操作。

## ? 快速启动

### Windows

**方法1：双击启动（推荐）**
- 在项目文件夹中找到 `run_gui.bat`
- 双击运行

**方法2：命令行启动**
```bash
python blog_manager_gui.py
```

### Linux / macOS

```bash
chmod +x run_gui.sh
./run_gui.sh
```

或直接使用Python：
```bash
python3 blog_manager_gui.py
```

## ? 系统要求

- **Python** 3.7+
- **tkinter** - Python标准库内置（无需额外安装）
- **Node.js & npm** - 用于VitePress预览和构建
- **Git** - 用于发布

## ? GUI 界面特性

### 6个功能标签页

| 标签页 | 功能 |
|--------|------|
| ? Dashboard | 实时统计、文章总数、总字数等 |
| ?? Articles | 创建新文章、列表管理、搜索过滤 |
| ?? Manage | 快速操作、构建、批量操作 |
| ?? Preview | 本地预览服务器控制 |
| ? Publish | 发布流程、一键发布 |
| ?? Settings | 项目信息、首选项、帮助 |

## ? 一键功能

### 创建文章
1. 进入 **?? Articles** 标签页
2. 填写标题、分类、描述
3. 点击 **创建**

### 编辑文章
1. 找到文章
2. 双击或右键选择 **编辑**

### 本地预览
1. 进入 **?? Preview** 标签页
2. 点击 **启动预览**
3. 访问 http://localhost:5173

### 一键发布
1. 进入 **? Publish** 标签页
2. 点击 **一键发布**
3. 自动完成：构建 → 提交 → 推送

## ? 完整文档

详细的使用指南请查看：

- **GUI 完整指南**：[GUI_GUIDE.md](GUI_GUIDE.md)
- **CLI 命令行版本**：[BLOG_MANAGER_README.md](BLOG_MANAGER_README.md)
- **快速开始**：[QUICK_START.md](QUICK_START.md)

## ? 使用提示

- ? 双击文章直接编辑
- ? 右键显示上下文菜单
- ? 搜索框快速过滤文章
- ? 实时显示操作日志
- ? 所有操作都可撤销

## ? 问题排查

### GUI 无法启动
```bash
# 检查Python版本
python --version

# 检查tkinter是否安装
python -m tkinter
```

### 找不到blog_manager
- 确保 `blog_manager.py` 在项目根目录
- 确保两个文件在同一目录

### 预览不工作
```bash
# 检查npm是否安装
npm --version

# 安装依赖
npm install
```

## ? 文件列表

```
项目根目录/
├── blog_manager.py              # CLI版本
├── blog_manager_gui.py          # GUI版本 (主程序)
├── run_gui.bat                  # Windows启动脚本
├── run_gui.sh                   # Linux/macOS启动脚本
├── GUI_GUIDE.md                 # GUI完整文档
├── BLOG_MANAGER_README.md       # CLI完整文档
└── QUICK_START.md               # 快速开始指南
```

## ? 对比

| 特性 | CLI | GUI |
|------|-----|-----|
| 学习成本 | 中 | 低 |
| 命令行 | ? | ? |
| 图形界面 | ? | ? |
| 功能 | 完整 | 完整 |
| 速度 | 快 | 快 |
| 易用性 | 中等 | 很好 |

---

**现在就开始使用吧！** ?

有问题？查看完整文档或提交Issue。
