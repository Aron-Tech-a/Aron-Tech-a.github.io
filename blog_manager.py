#!/usr/bin/env python3
"""
VitePress Blog Manager - Python CLI应用
方便管理VitePress博客的创建、编辑、预览和发布
"""

import os
import sys
import argparse
import subprocess
from datetime import datetime
from pathlib import Path
import json
from typing import Optional

# On Windows, shell=True is required so that .cmd scripts (npm.cmd, git.cmd)
# registered in PATH are found by subprocess.
_SHELL = sys.platform == "win32"


class BlogManager:
    """博客管理器类"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.docs_dir = self.project_root / "docs"
        self.vitepress_config = self.project_root / "docs" / ".vitepress" / "config.mts"
        
        # 验证VitePress项目
        if not self.docs_dir.exists():
            raise FileNotFoundError(f"docs目录不存在: {self.docs_dir}")
    
    def create_article(self, title: str, category: Optional[str] = None, 
                       description: str = "") -> Path:
        """创建新的博客文章
        
        Args:
            title: 文章标题
            category: 文章分类（可选，如'ble', 'examples'）
            description: 文章描述
            
        Returns:
            创建的文件路径
        """
        # 生成文件名：将标题转换为URL友好的格式
        filename = title.lower().replace(" ", "-").replace("_", "-")
        filename = "".join(c if c.isalnum() or c == "-" else "" for c in filename)
        
        # 确定目录
        if category:
            article_dir = self.docs_dir / category
            article_dir.mkdir(parents=True, exist_ok=True)
        else:
            article_dir = self.docs_dir
        
        article_path = article_dir / f"{filename}.md"
        
        # 检查文件是否已存在
        if article_path.exists():
            print(f"❌ 文件已存在: {article_path}")
            return article_path
        
        # 生成Markdown模板
        template = f"""# {title}

> {description if description else '文章描述'}

**发布时间**: {datetime.now().strftime('%Y-%m-%d')}

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
"""
        
        # 写入文件
        with open(article_path, 'w', encoding='utf-8') as f:
            f.write(template)
        
        print(f"✅ 文章创建成功: {article_path}")
        return article_path
    
    def list_articles(self, category: Optional[str] = None) -> list:
        """列出所有博客文章
        
        Args:
            category: 指定分类（可选）
            
        Returns:
            文章路径列表
        """
        if category:
            search_dir = self.docs_dir / category
            if not search_dir.exists():
                print(f"❌ 分类不存在: {category}")
                return []
        else:
            search_dir = self.docs_dir
        
        articles = []
        for md_file in search_dir.rglob("*.md"):
            # 排除.vitepress目录
            if ".vitepress" not in str(md_file):
                rel_path = md_file.relative_to(self.docs_dir)
                articles.append(md_file)
                print(f"📄 {rel_path}")
        
        if not articles:
            print("📭 没有找到文章")
        else:
            print(f"\n共找到 {len(articles)} 篇文章")
        
        return articles
    
    def open_article(self, article_path: str) -> None:
        """打开文章进行编辑（使用默认编辑器）
        
        Args:
            article_path: 文章相对路径或文件名
        """
        full_path = self.docs_dir / article_path
        
        if not full_path.exists():
            # 尝试查找匹配的文件
            matches = list(self.docs_dir.rglob(f"*{article_path}*.md"))
            if matches:
                full_path = matches[0]
            else:
                print(f"❌ 文件不存在: {article_path}")
                return
        
        # Windows, macOS, Linux上打开文件
        if sys.platform == "win32":
            os.startfile(str(full_path))
        elif sys.platform == "darwin":
            subprocess.run(["open", str(full_path)])
        else:
            subprocess.run(["xdg-open", str(full_path)])
        
        print(f"📖 打开文件: {full_path}")
    
    def preview(self, port: int = 5173) -> None:
        """启动本地预览服务器
        
        Args:
            port: 预览服务器端口
        """
        print(f"🚀 启动VitePress开发服务器 (http://localhost:{port})...")
        try:
            subprocess.run(["npm", "run", "docs:dev"], cwd=self.project_root, shell=_SHELL)
        except KeyboardInterrupt:
            print("\n⏹️  开发服务器已停止")
        except Exception as e:
            print(f"❌ 启动失败: {e}")
    
    def build(self) -> bool:
        """构建静态站点
        
        Returns:
            构建是否成功
        """
        print("🔨 开始构建VitePress站点...")
        try:
            result = subprocess.run(
                ["npm", "run", "docs:build"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                shell=_SHELL
            )
            if result.returncode == 0:
                print("✅ 站点构建成功!")
                return True
            else:
                print(f"❌ 构建失败:\n{result.stderr}")
                return False
        except Exception as e:
            print(f"❌ 构建出错: {e}")
            return False
    
    def publish(self, message: str = "Update blog content") -> bool:
        """提交并推送更改到GitHub
        
        Args:
            message: 提交消息
            
        Returns:
            是否成功
        """
        try:
            # 添加所有更改
            print("📦 添加文件...")
            subprocess.run(["git", "add", "."], cwd=self.project_root, check=True, shell=_SHELL)
            
            # 提交
            print("💾 提交更改...")
            subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.project_root,
                check=True,
                shell=_SHELL
            )
            
            # 推送
            print("⬆️  推送到GitHub...")
            subprocess.run(["git", "push"], cwd=self.project_root, check=True, shell=_SHELL)
            
            print("✅ 发布成功!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 发布失败: {e}")
            return False
        except Exception as e:
            print(f"❌ 错误: {e}")
            return False
    
    def get_article_stats(self) -> dict:
        """获取博客统计信息
        
        Returns:
            统计信息字典
        """
        articles = list(self.docs_dir.rglob("*.md"))
        articles = [f for f in articles if ".vitepress" not in str(f)]
        
        total_words = 0
        for article in articles:
            with open(article, 'r', encoding='utf-8') as f:
                total_words += len(f.read().split())
        
        stats = {
            "total_articles": len(articles),
            "total_words": total_words,
            "avg_words_per_article": total_words // len(articles) if articles else 0
        }
        return stats
    
    def show_stats(self) -> None:
        """显示博客统计信息"""
        stats = self.get_article_stats()
        print("\n📊 博客统计信息")
        print(f"  📝 文章总数: {stats['total_articles']}")
        print(f"  📚 总字数: {stats['total_words']:,}")
        print(f"  📄 平均字数: {stats['avg_words_per_article']}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="VitePress博客管理器 - 用Python方便地管理您的博客",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python blog_manager.py create "我的第一篇文章" --category ble --description "一篇关于BLE的文章"
  python blog_manager.py list
  python blog_manager.py list --category ble
  python blog_manager.py open ble/ananlyzer.md
  python blog_manager.py preview
  python blog_manager.py build
  python blog_manager.py publish --message "Add new article"
  python blog_manager.py stats
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # 创建文章
    create_parser = subparsers.add_parser("create", help="创建新的博客文章")
    create_parser.add_argument("title", help="文章标题")
    create_parser.add_argument("--category", help="文章分类（可选）")
    create_parser.add_argument("--description", default="", help="文章描述")
    
    # 列出文章
    list_parser = subparsers.add_parser("list", help="列出所有博客文章")
    list_parser.add_argument("--category", help="指定分类（可选）")
    
    # 打开文章
    open_parser = subparsers.add_parser("open", help="打开文章进行编辑")
    open_parser.add_argument("article", help="文章路径或文件名")
    
    # 预览
    preview_parser = subparsers.add_parser("preview", help="启动本地预览服务器")
    preview_parser.add_argument("--port", type=int, default=5173, help="服务器端口")
    
    # 构建
    subparsers.add_parser("build", help="构建静态站点")
    
    # 发布
    publish_parser = subparsers.add_parser("publish", help="提交并推送到GitHub")
    publish_parser.add_argument("--message", "-m", default="Update blog content", help="提交消息")
    
    # 统计
    subparsers.add_parser("stats", help="显示博客统计信息")
    
    args = parser.parse_args()
    
    try:
        # 获取项目根目录
        project_root = Path.cwd()
        manager = BlogManager(str(project_root))
        
        if args.command == "create":
            manager.create_article(
                args.title,
                category=args.category,
                description=args.description
            )
        elif args.command == "list":
            manager.list_articles(category=args.category)
        elif args.command == "open":
            manager.open_article(args.article)
        elif args.command == "preview":
            manager.preview(port=args.port)
        elif args.command == "build":
            manager.build()
        elif args.command == "publish":
            manager.publish(message=args.message)
        elif args.command == "stats":
            manager.show_stats()
        else:
            parser.print_help()
    
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
