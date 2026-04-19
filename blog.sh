#!/bin/bash
# VitePress Blog Manager - Linux/macOS 启动脚本
# 用法: ./blog.sh create "文章标题" [--category 分类]
#       ./blog.sh list [--category 分类]
#       ./blog.sh preview
#       ./blog.sh publish --message "提交消息"
#       等等...

if [ $# -eq 0 ]; then
    echo "VitePress 博客管理器"
    echo ""
    echo "命令:"
    echo "  ./blog.sh create \"标题\"           - 创建新文章"
    echo "  ./blog.sh list                    - 列出所有文章"
    echo "  ./blog.sh open <文件名>           - 打开文章编辑"
    echo "  ./blog.sh preview                 - 本地预览"
    echo "  ./blog.sh build                   - 构建站点"
    echo "  ./blog.sh publish                 - 发布到GitHub"
    echo "  ./blog.sh stats                   - 显示统计信息"
    echo ""
    echo "查看详细帮助: python blog_manager.py -h"
    exit 0
fi

python3 blog_manager.py "$@"
