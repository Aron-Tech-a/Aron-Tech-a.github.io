@echo off
REM VitePress Blog Manager - Windows启动脚本
REM 用法: blog create "文章标题" [--category 分类]
REM       blog list [--category 分类]
REM       blog preview
REM       blog publish --message "提交消息"
REM       等等...

if "%1"=="" (
    echo VitePress 博客管理器
    echo.
    echo 命令:
    echo   blog create "标题"           - 创建新文章
    echo   blog list                    - 列出所有文章
    echo   blog open ^<文件名^>          - 打开文章编辑
    echo   blog preview                 - 本地预览
    echo   blog build                   - 构建站点
    echo   blog publish                 - 发布到GitHub
    echo   blog stats                   - 显示统计信息
    echo.
    echo 查看详细帮助: python blog_manager.py -h
    exit /b 0
)

python blog_manager.py %*
