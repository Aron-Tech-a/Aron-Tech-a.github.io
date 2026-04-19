# -*- coding: utf-8 -*-
"""
VitePress Blog Manager GUI
A graphical user interface for managing VitePress blogs
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import tkinter.font as tkFont
from pathlib import Path
from datetime import datetime
import subprocess
import threading
import os
import sys
from typing import Optional, List
import json

# On Windows, shell=True is required so that .cmd scripts (npm.cmd, git.cmd)
# registered in PATH are found by subprocess.
_SHELL = sys.platform == "win32"

# Import blog manager core functions
sys.path.insert(0, str(Path(__file__).parent))
from blog_manager import BlogManager


class BlogManagerGUI:
    """博客管理器GUI应用"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("VitePress 博客管理器")
        self.root.geometry("1200x700")
        self.root.minsize(900, 600)
        
        # 初始化博客管理器
        try:
            self.manager = BlogManager(str(Path.cwd()))
        except FileNotFoundError as e:
            messagebox.showerror("错误", f"无法找到VitePress项目:\n{e}")
            return
        
        # 设置样式
        self.setup_styles()
        
        # 创建GUI
        self.create_widgets()
        self.refresh_article_list()
        self.update_stats()
    
    def setup_styles(self):
        """设置UI样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 颜色方案
        self.bg_color = "#f0f0f0"
        self.accent_color = "#2196F3"
        self.success_color = "#4CAF50"
        self.warning_color = "#FF9800"
        self.error_color = "#f44336"
        
        # 字体
        self.title_font = tkFont.Font(family="Segoe UI", size=14, weight="bold")
        self.normal_font = tkFont.Font(family="Segoe UI", size=10)
        self.small_font = tkFont.Font(family="Segoe UI", size=9)
    
    def create_widgets(self):
        """创建主要Widget"""
        # 主容器
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建Notebook（标签页）
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 各个标签页
        self.create_dashboard_tab()
        self.create_article_tab()
        self.create_manage_tab()
        self.create_preview_tab()
        self.create_publish_tab()
        self.create_settings_tab()
    
    def create_dashboard_tab(self):
        """仪表板标签页"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📊 仪表板")
        
        # 标题
        title_frame = ttk.Frame(tab)
        title_frame.pack(fill=tk.X, padx=20, pady=20)
        
        title_label = ttk.Label(title_frame, text="博客统计信息", font=self.title_font)
        title_label.pack()
        
        # 统计卡片
        cards_frame = ttk.Frame(tab)
        cards_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 创建统计卡片
        self.stat_frames = {}
        stat_data = [
            ("total_articles", "📝 文章总数", "0"),
            ("total_words", "📚 总字数", "0"),
            ("avg_words", "📄 平均字数", "0")
        ]
        
        for stat_key, label, default in stat_data:
            card_frame = self.create_stat_card(cards_frame, label, default)
            self.stat_frames[stat_key] = card_frame
            card_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 最近文章
        recent_frame = ttk.LabelFrame(tab, text="最近修改的文章", padding=15)
        recent_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 最近文章列表
        self.recent_text = scrolledtext.ScrolledText(
            recent_frame, height=12, width=50, state=tk.DISABLED
        )
        self.recent_text.pack(fill=tk.BOTH, expand=True)
        
        # 刷新按钮
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(btn_frame, text="🔄 刷新", command=self.update_stats).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="📂 打开文件夹", command=self.open_docs_folder).pack(side=tk.LEFT, padx=5)
    
    def create_stat_card(self, parent, label: str, value: str) -> tk.Frame:
        """创建统计卡片"""
        card = tk.Frame(parent, bg="white", relief=tk.RAISED, bd=1)
        card.pack_propagate(False)
        
        label_widget = ttk.Label(card, text=label, font=self.normal_font)
        label_widget.pack(pady=10)
        
        self.stat_value = ttk.Label(card, text=value, font=("Segoe UI", 24, "bold"))
        self.stat_value.pack(pady=10)
        
        card.stat_value = self.stat_value
        return card
    
    def create_article_tab(self):
        """文章管理标签页"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="✍️ 文章管理")
        
        # 上面板：创建新文章
        create_frame = ttk.LabelFrame(tab, text="创建新文章", padding=15)
        create_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 标题输入
        ttk.Label(create_frame, text="文章标题:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.title_entry = ttk.Entry(create_frame, width=40)
        self.title_entry.grid(row=0, column=1, sticky=tk.EW, padx=5)
        
        # 分类选择
        ttk.Label(create_frame, text="分类:").grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
        self.category_var = tk.StringVar(value="")
        self.category_combo = ttk.Combobox(
            create_frame, 
            textvariable=self.category_var,
            values=["", "ble", "tutorials", "examples"],
            state="readonly",
            width=15
        )
        self.category_combo.grid(row=0, column=3, sticky=tk.EW, padx=5)
        
        # 描述输入
        ttk.Label(create_frame, text="描述:").grid(row=1, column=0, sticky=tk.NW, pady=5)
        self.desc_text = scrolledtext.ScrolledText(create_frame, height=4, width=60)
        self.desc_text.grid(row=1, column=1, columnspan=3, sticky=tk.EW, padx=5, pady=5)
        
        # 创建按钮
        btn_frame = ttk.Frame(create_frame)
        btn_frame.grid(row=2, column=0, columnspan=4, sticky=tk.EW, pady=10)
        ttk.Button(btn_frame, text="➕ 创建文章", command=self.create_article).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🔄 清空", command=self.clear_create_form).pack(side=tk.LEFT, padx=5)
        
        create_frame.columnconfigure(1, weight=1)
        create_frame.columnconfigure(3, weight=1)
        
        # 下面板：文章列表
        list_frame = ttk.LabelFrame(tab, text="文章列表", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 搜索框
        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="搜索:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.filter_articles())
        
        ttk.Button(search_frame, text="🔄 刷新", command=self.refresh_article_list).pack(side=tk.LEFT, padx=5)
        
        # 文章列表（Treeview）
        columns = ("名称", "路径", "大小")
        self.article_tree = ttk.Treeview(list_frame, columns=columns, height=15)
        self.article_tree.column("#0", width=30)
        self.article_tree.column("名称", width=200)
        self.article_tree.column("路径", width=250)
        self.article_tree.column("大小", width=80)
        
        self.article_tree.heading("#0", text="")
        self.article_tree.heading("名称", text="文件名")
        self.article_tree.heading("路径", text="路径")
        self.article_tree.heading("大小", text="字数")
        
        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.article_tree.yview)
        self.article_tree.configure(yscroll=scrollbar.set)
        
        self.article_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 右键菜单
        self.article_tree.bind("<Button-3>", self.show_article_context_menu)
        self.article_tree.bind("<Double-1>", lambda e: self.open_article_editor())
    
    def create_manage_tab(self):
        """管理标签页"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚙️ 管理")
        
        # 操作面板
        ops_frame = ttk.LabelFrame(tab, text="快速操作", padding=20)
        ops_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 按钮网格
        buttons = [
            ("📖 打开文章", self.open_article_editor),
            ("✏️ 编辑文章", self.edit_selected_article),
            ("🗑️ 删除文章", self.delete_article),
            ("📁 打开文件夹", self.open_docs_folder),
            ("🔍 打开docs目录", self.open_in_explorer),
        ]
        
        for i, (text, cmd) in enumerate(buttons):
            row, col = divmod(i, 3)
            btn = ttk.Button(ops_frame, text=text, command=cmd, width=20)
            btn.grid(row=row, column=col, padx=10, pady=10, sticky=tk.EW)
        
        # 批量操作
        batch_frame = ttk.LabelFrame(tab, text="批量操作", padding=20)
        batch_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(batch_frame, text="🔨 构建项目", command=self.build_project, width=30).pack(side=tk.LEFT, padx=5)
        ttk.Button(batch_frame, text="🧹 清理", command=self.clean_project, width=30).pack(side=tk.LEFT, padx=5)
        
        # 日志显示
        log_frame = ttk.LabelFrame(tab, text="操作日志", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # 清空日志按钮
        ttk.Button(tab, text="清空日志", command=self.clear_logs).pack(pady=5)
    
    def create_preview_tab(self):
        """预览标签页"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="👁️ 预览")
        
        # 预览控制
        ctrl_frame = ttk.Frame(tab)
        ctrl_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(ctrl_frame, text="预览服务器:").pack(side=tk.LEFT, padx=5)
        
        self.preview_status = ttk.Label(ctrl_frame, text="● 已停止", foreground="red")
        self.preview_status.pack(side=tk.LEFT, padx=5)
        
        self.preview_btn = ttk.Button(ctrl_frame, text="▶️ 启动预览", command=self.start_preview)
        self.preview_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_preview_btn = ttk.Button(ctrl_frame, text="⏹️ 停止", command=self.stop_preview, state=tk.DISABLED)
        self.stop_preview_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(ctrl_frame, text="http://localhost:5173", foreground="blue").pack(side=tk.LEFT, padx=20)
        
        # 预览信息
        info_frame = ttk.LabelFrame(tab, text="预览信息", padding=15)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.preview_info = scrolledtext.ScrolledText(info_frame, height=20, state=tk.DISABLED)
        self.preview_info.pack(fill=tk.BOTH, expand=True)
        
        self.preview_process = None
    
    def create_publish_tab(self):
        """发布标签页"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🚀 发布")
        
        # 发布步骤
        steps_frame = ttk.LabelFrame(tab, text="发布步骤", padding=15)
        steps_frame.pack(fill=tk.X, padx=10, pady=10)
        
        steps = [
            ("1️⃣", "构建站点", self.build_and_publish, "build"),
            ("2️⃣", "预览更改", self.preview_changes, "preview"),
            ("3️⃣", "提交代码", self.commit_changes, "commit"),
            ("4️⃣", "推送远程", self.push_changes, "push"),
        ]
        
        self.publish_steps = {}
        for i, (emoji, text, cmd, key) in enumerate(steps):
            step_frame = ttk.Frame(steps_frame)
            step_frame.pack(fill=tk.X, pady=5)
            
            status = tk.StringVar(value="⭕")
            self.publish_steps[key] = {"var": status, "frame": step_frame}
            
            status_label = ttk.Label(step_frame, textvariable=status, font=("Arial", 12))
            status_label.pack(side=tk.LEFT, padx=5)
            
            ttk.Label(step_frame, text=text, font=self.normal_font).pack(side=tk.LEFT, padx=5)
            ttk.Button(step_frame, text="执行", command=cmd, width=15).pack(side=tk.RIGHT, padx=5)
        
        # 提交消息
        msg_frame = ttk.LabelFrame(tab, text="提交消息", padding=15)
        msg_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(msg_frame, text="消息:").pack(side=tk.LEFT, padx=5)
        self.commit_msg = ttk.Entry(msg_frame)
        self.commit_msg.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.commit_msg.insert(0, "Update blog content")
        
        # 一键发布
        publish_frame = ttk.Frame(tab)
        publish_frame.pack(fill=tk.X, padx=10, pady=15)
        
        ttk.Button(
            publish_frame, 
            text="🚀 一键发布", 
            command=self.one_click_publish,
            width=30
        ).pack(side=tk.LEFT, padx=5)
        
        # 发布日志
        log_frame = ttk.LabelFrame(tab, text="发布日志", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.publish_log = scrolledtext.ScrolledText(log_frame, height=15, state=tk.DISABLED)
        self.publish_log.pack(fill=tk.BOTH, expand=True)
    
    def create_settings_tab(self):
        """设置标签页"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚙️ 设置")
        
        # 项目信息
        info_frame = ttk.LabelFrame(tab, text="项目信息", padding=15)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        info_text = f"""
项目路径: {self.manager.project_root}
Docs目录: {self.manager.docs_dir}
VitePress配置: {self.manager.vitepress_config}
        """
        
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT, font=self.small_font).pack(fill=tk.X)
        
        # 首选项
        prefs_frame = ttk.LabelFrame(tab, text="首选项", padding=15)
        prefs_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.auto_build = tk.BooleanVar(value=False)
        ttk.Checkbutton(prefs_frame, text="发布前自动构建", variable=self.auto_build).pack(anchor=tk.W, pady=5)
        
        self.auto_commit = tk.BooleanVar(value=False)
        ttk.Checkbutton(prefs_frame, text="保存时自动提交", variable=self.auto_commit).pack(anchor=tk.W, pady=5)
        
        # 帮助
        help_frame = ttk.LabelFrame(tab, text="帮助", padding=15)
        help_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        help_text = """
快速提示:
• 双击文章可直接编辑
• 右键文章可查看选项
• 预览需要npm环境
• 发布需要Git配置
• 所有操作都是可撤销的

快捷键:
• Ctrl+N: 新建文章
• Ctrl+S: 保存
• Ctrl+R: 刷新

有问题?
• 查看 BLOG_MANAGER_README.md
• 查看 QUICK_START.md
        """
        
        help_widget = scrolledtext.ScrolledText(help_frame, height=15, state=tk.DISABLED)
        help_widget.pack(fill=tk.BOTH, expand=True)
        help_widget.config(state=tk.NORMAL)
        help_widget.insert(tk.END, help_text)
        help_widget.config(state=tk.DISABLED)
    
    # ========== 事件处理 ==========
    
    def create_article(self):
        """创建新文章"""
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showwarning("警告", "请输入文章标题")
            return
        
        category = self.category_var.get() or None
        description = self.desc_text.get("1.0", tk.END).strip()
        
        try:
            self.manager.create_article(title, category=category, description=description)
            messagebox.showinfo("成功", "文章创建成功！")
            self.clear_create_form()
            self.refresh_article_list()
            self.log_message(f"✅ 创建文章: {title}")
        except Exception as e:
            messagebox.showerror("错误", f"创建失败: {e}")
            self.log_message(f"❌ 创建失败: {e}")
    
    def clear_create_form(self):
        """清空创建表单"""
        self.title_entry.delete(0, tk.END)
        self.category_var.set("")
        self.desc_text.delete("1.0", tk.END)
    
    def refresh_article_list(self):
        """刷新文章列表"""
        # 清空树
        for item in self.article_tree.get_children():
            self.article_tree.delete(item)
        
        # 获取所有文章
        articles = self.manager.list_articles()
        
        for article_path in articles:
            rel_path = str(article_path.relative_to(self.manager.docs_dir))
            
            # 获取文件信息
            file_size = article_path.stat().st_size
            with open(article_path, 'r', encoding='utf-8') as f:
                word_count = len(f.read().split())
            
            filename = article_path.name
            
            self.article_tree.insert(
                "", "end",
                values=(filename, rel_path, str(word_count))
            )
    
    def filter_articles(self):
        """过滤文章"""
        search_text = self.search_entry.get().lower()
        
        for item in self.article_tree.get_children():
            values = self.article_tree.item(item, "values")
            if search_text in values[0].lower() or search_text in values[1].lower():
                self.article_tree.item(item, tags=())
            else:
                self.article_tree.item(item, tags=("hidden",))
        
        self.article_tree.tag_configure("hidden", foreground="#cccccc")
    
    def show_article_context_menu(self, event):
        """显示文章右键菜单"""
        item = self.article_tree.identify("item", event.x, event.y)
        if not item:
            return
        
        self.article_tree.selection_set(item)
        
        menu = tk.Menu(self.root, tearoff=False)
        menu.add_command(label="📖 打开", command=self.open_article_editor)
        menu.add_command(label="✏️ 编辑", command=self.edit_selected_article)
        menu.add_separator()
        menu.add_command(label="🗑️ 删除", command=self.delete_article)
        menu.add_separator()
        menu.add_command(label="📋 复制路径", command=self.copy_article_path)
        
        menu.post(event.x_root, event.y_root)
    
    def open_article_editor(self):
        """打开文章编辑器"""
        selection = self.article_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择一篇文章")
            return
        
        item = selection[0]
        values = self.article_tree.item(item, "values")
        article_path = values[1]
        
        try:
            self.manager.open_article(article_path)
            self.log_message(f"📖 打开文章: {article_path}")
        except Exception as e:
            messagebox.showerror("错误", f"打开失败: {e}")
    
    def edit_selected_article(self):
        """编辑选中的文章"""
        self.open_article_editor()
    
    def delete_article(self):
        """删除文章"""
        selection = self.article_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择一篇文章")
            return
        
        item = selection[0]
        values = self.article_tree.item(item, "values")
        filename = values[0]
        article_path = values[1]
        
        if messagebox.askyesno("确认", f"确定要删除 '{filename}' 吗？"):
            full_path = self.manager.docs_dir / article_path
            try:
                full_path.unlink()
                self.article_tree.delete(item)
                self.log_message(f"🗑️ 删除文章: {article_path}")
                messagebox.showinfo("成功", "文章已删除")
                self.refresh_article_list()
            except Exception as e:
                messagebox.showerror("错误", f"删除失败: {e}")
    
    def copy_article_path(self):
        """复制文章路径"""
        selection = self.article_tree.selection()
        if selection:
            values = self.article_tree.item(selection[0], "values")
            self.root.clipboard_clear()
            self.root.clipboard_append(values[1])
            messagebox.showinfo("成功", "路径已复制到剪贴板")
    
    def open_docs_folder(self):
        """打开docs文件夹"""
        try:
            if sys.platform == "win32":
                os.startfile(str(self.manager.docs_dir))
            elif sys.platform == "darwin":
                subprocess.run(["open", str(self.manager.docs_dir)])
            else:
                subprocess.run(["xdg-open", str(self.manager.docs_dir)])
            self.log_message(f"📁 打开文件夹: {self.manager.docs_dir}")
        except Exception as e:
            messagebox.showerror("错误", f"打开失败: {e}")
    
    def open_in_explorer(self):
        """在资源管理器中打开"""
        self.open_docs_folder()
    
    def build_project(self):
        """构建项目"""
        self.log_message("🔨 开始构建项目...")
        
        def build_thread():
            result = self.manager.build()
            if result:
                self.log_message("✅ 构建成功!")
                messagebox.showinfo("成功", "项目构建成功")
            else:
                self.log_message("❌ 构建失败")
                messagebox.showerror("错误", "项目构建失败")
        
        thread = threading.Thread(target=build_thread, daemon=True)
        thread.start()
    
    def clean_project(self):
        """清理项目"""
        if messagebox.askyesno("确认", "确定要清理项目吗？"):
            self.log_message("🧹 清理项目...")
            try:
                subprocess.run(
                    ["npm", "run", "clean"],
                    cwd=self.manager.project_root,
                    capture_output=True,
                    shell=_SHELL
                )
                self.log_message("✅ 清理完成")
            except:
                self.log_message("⚠️ 清理命令不可用")
    
    def start_preview(self):
        """启动预览"""
        self.log_message("🚀 启动预览服务器...")
        self.preview_status.config(text="● 运行中...", foreground="green")
        self.preview_btn.config(state=tk.DISABLED)
        self.stop_preview_btn.config(state=tk.NORMAL)
        
        def preview_thread():
            try:
                self.preview_process = subprocess.Popen(
                    ["npm", "run", "docs:dev"],
                    cwd=self.manager.project_root,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    shell=_SHELL
                )
                
                for line in self.preview_process.stdout:
                    self.add_preview_info(line.strip())
            except Exception as e:
                self.add_preview_info(f"❌ 错误: {e}")
        
        thread = threading.Thread(target=preview_thread, daemon=True)
        thread.start()
        
        self.add_preview_info("✅ 预览服务器已启动")
        self.add_preview_info("访问: http://localhost:5173")
    
    def stop_preview(self):
        """停止预览"""
        if self.preview_process:
            self.preview_process.terminate()
            self.preview_process = None
        
        self.preview_status.config(text="● 已停止", foreground="red")
        self.preview_btn.config(state=tk.NORMAL)
        self.stop_preview_btn.config(state=tk.DISABLED)
        self.add_preview_info("⏹️  预览服务器已停止")
    
    def build_and_publish(self):
        """构建并发布"""
        self.update_publish_step("build", "🔄")
        self.build_project()
        self.update_publish_step("build", "✅")
    
    def preview_changes(self):
        """预览更改"""
        self.update_publish_step("preview", "🔄")
        self.publish_log_message("📋 预览更改...")
        self.update_publish_step("preview", "✅")
    
    def commit_changes(self):
        """提交更改"""
        self.update_publish_step("commit", "🔄")
        self.publish_log_message("💾 提交更改...")
        
        message = self.commit_msg.get()
        try:
            subprocess.run(["git", "add", "."], cwd=self.manager.project_root, check=True, shell=_SHELL)
            subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.manager.project_root,
                check=True,
                shell=_SHELL
            )
            self.publish_log_message("✅ 提交成功")
            self.update_publish_step("commit", "✅")
        except Exception as e:
            self.publish_log_message(f"❌ 提交失败: {e}")
            self.update_publish_step("commit", "❌")
    
    def push_changes(self):
        """推送更改"""
        self.update_publish_step("push", "🔄")
        self.publish_log_message("⬆️  推送到远程...")
        
        try:
            subprocess.run(["git", "push"], cwd=self.manager.project_root, check=True, shell=_SHELL)
            self.publish_log_message("✅ 推送成功")
            self.update_publish_step("push", "✅")
        except Exception as e:
            self.publish_log_message(f"❌ 推送失败: {e}")
            self.update_publish_step("push", "❌")
    
    def one_click_publish(self):
        """一键发布"""
        self.publish_log_message("🚀 开始一键发布流程...")
        self.build_and_publish()
        self.commit_changes()
        self.push_changes()
        self.publish_log_message("✅ 发布完成！")
    
    def update_stats(self):
        """更新统计信息"""
        stats = self.manager.get_article_stats()
        
        self.stat_frames["total_articles"].stat_value.config(
            text=str(stats["total_articles"])
        )
        self.stat_frames["total_words"].stat_value.config(
            text=f"{stats['total_words']:,}"
        )
        self.stat_frames["avg_words"].stat_value.config(
            text=str(stats["avg_words_per_article"])
        )
    
    def log_message(self, message: str):
        """添加日志消息"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def add_preview_info(self, info: str):
        """添加预览信息"""
        self.preview_info.config(state=tk.NORMAL)
        self.preview_info.insert(tk.END, f"{info}\n")
        self.preview_info.see(tk.END)
        self.preview_info.config(state=tk.DISABLED)
    
    def publish_log_message(self, message: str):
        """添加发布日志"""
        self.publish_log.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.publish_log.insert(tk.END, f"[{timestamp}] {message}\n")
        self.publish_log.see(tk.END)
        self.publish_log.config(state=tk.DISABLED)
    
    def update_publish_step(self, step: str, status: str):
        """更新发布步骤状态"""
        if step in self.publish_steps:
            self.publish_steps[step]["var"].set(status)
    
    def clear_logs(self):
        """清空日志"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state=tk.DISABLED)


def main():
    """主函数"""
    root = tk.Tk()
    
    # 设置窗口图标（如果可用）
    try:
        root.iconbitmap("blog_icon.ico")
    except:
        pass
    
    app = BlogManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
