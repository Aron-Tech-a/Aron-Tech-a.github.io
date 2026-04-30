# Windows 上安装、运行与测试 MinerU：从 Python 3.12 到 GPU 加速和 DOCX 输出

本文记录一次在 Windows 环境下安装、运行、测试 MinerU 的完整过程，包括环境准备、常见问题修复、GPU 加速、批量解析 PDF，以及将 MinerU 输出的 Markdown 转换为 DOCX 文档。

示例环境：

- 系统：Windows
- 项目目录：`E:\MinerU\MinerU`
- Python：3.12
- GPU：NVIDIA GeForce RTX 4060 Laptop GPU，约 8GB 显存
- MinerU：3.1.6，本地源码安装

## 1. 为什么选择 Python 3.12

MinerU 的 `pyproject.toml` 声明支持 Python `>=3.10,<3.14`，但在 Windows 上需要特别注意：关键依赖 `ray` 对 Python 3.13 的支持存在限制。因此，Windows 平台建议使用 Python 3.10 到 3.12。

本次环境最初 VS Code 检测到系统 Python 是 3.13，但为了避免依赖兼容性问题，改用 Python 3.12 创建项目虚拟环境。

## 2. 创建虚拟环境

进入项目目录：

```powershell
cd E:\MinerU\MinerU
```

使用 Python 3.12 创建虚拟环境：

```powershell
py -3.12 -m venv .venv
```

激活虚拟环境：

```powershell
.\.venv\Scripts\Activate.ps1
```

如果 PowerShell 拦截脚本执行，可以只对当前进程放开执行策略：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

升级 pip 并安装 uv：

```powershell
python -m pip install -U pip
pip install uv
```

## 3. 从源码安装 MinerU

在项目根目录执行：

```powershell
uv pip install -e ".[all]"
```

安装过程中可能出现类似提示：

```text
warning: Failed to hardlink files; falling back to full copy.
```

这是 uv 缓存和目标目录不在同一文件系统时常见的性能提示，不影响安装结果。

安装完成后可确认命令是否可用：

```powershell
mineru --help
mineru-api --help
mineru-gradio --help
```

MinerU 安装后常用命令包括：

- `mineru`：命令行解析入口
- `mineru-api`：FastAPI 服务
- `mineru-router`：多服务/多 GPU 路由入口
- `mineru-gradio`：Gradio WebUI
- `mineru-models-download`：模型下载入口

## 4. 启动 MinerU API 服务

启动本地 API：

```powershell
mineru-api --host 127.0.0.1 --port 8000
```

正常启动后会看到：

```text
Start MinerU FastAPI Service: http://127.0.0.1:8000
API documentation: http://127.0.0.1:8000/docs
Uvicorn running on http://127.0.0.1:8000
```

浏览器访问根路径 `/` 返回 `404 Not Found` 是正常的，因为服务入口不是主页，而是 API 接口。可用健康检查接口确认服务状态：

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health | ConvertTo-Json
```

正常结果类似：

```json
{
  "status": "healthy",
  "version": "3.1.6",
  "protocol_version": 1,
  "queued_tasks": 0,
  "processing_tasks": 0,
  "completed_tasks": 0,
  "failed_tasks": 0,
  "max_concurrent_requests": 3,
  "processing_window_size": 64
}
```

## 5. 先做单文件、单页冒烟测试

项目自带测试 PDF 位于：

```text
demo\pdfs\
  demo1.pdf
  demo2.pdf
  demo3.pdf
  small_ocr.pdf
```

首次测试建议只跑 `small_ocr.pdf` 的第一页，降低排查成本：

```powershell
mineru -p .\demo\pdfs\small_ocr.pdf -o .\output_test_single -b pipeline -m ocr -s 0 -e 0 --api-url http://127.0.0.1:8000
```

参数说明：

- `-p`：输入文件或目录
- `-o`：输出目录
- `-b pipeline`：使用 pipeline 后端，兼容性最好
- `-m ocr`：强制 OCR 模式
- `-s 0 -e 0`：只处理第 1 页，页码从 0 开始
- `--api-url`：连接已有的本地 API 服务

成功时会看到：

```text
Completed batch 1/1 | Processed 1/1 page
```

输出目录示例：

```text
output_test_single\small_ocr\ocr\
  small_ocr.md
  small_ocr_content_list.json
  small_ocr_content_list_v2.json
  small_ocr_layout.pdf
  small_ocr_middle.json
  small_ocr_model.json
  small_ocr_origin.pdf
  small_ocr_span.pdf
```

其中：

- `*.md`：主要 Markdown 输出
- `*_content_list.json`：按阅读顺序组织的内容列表
- `*_middle.json`：中间结构数据
- `*_model.json`：模型原始/中间输出
- `*_layout.pdf`：版面检测可视化
- `*_span.pdf`：span 级别可视化
- `images/`：截图、图片、表格、公式等资源

## 6. 首次运行超时的原因与处理

第一次解析整个 `demo\pdfs` 目录时，可能出现超时：

```text
Timed out waiting for result of task ...
```

这通常不是解析失败，而是首次运行需要下载和初始化模型。日志中可以看到模型文件下载，例如：

```text
model.safetensors: 810M
model.safetensors: 215M
ch_PP-OCRv5_det_infer.pth
ch_PP-OCRv5_rec_infer.pth
unet.onnx
```

处理建议：

1. 首次运行先测试单文件、单页。
2. 等模型下载完成后再跑多文件。
3. 如果客户端等待超时，但 API 端任务仍在处理，可通过任务 ID 查询状态。

查询任务状态示例：

```powershell
Invoke-RestMethod http://127.0.0.1:8000/tasks/<task_id> | ConvertTo-Json -Depth 5
```

如果任务状态是 `completed`，可下载结果：

```powershell
Invoke-WebRequest -Uri http://127.0.0.1:8000/tasks/<task_id>/result -OutFile result.zip
Expand-Archive -Path result.zip -DestinationPath .\output_from_task -Force
```

## 7. 启用 GPU 加速

### 7.1 检查显卡驱动

执行：

```powershell
nvidia-smi
```

本次机器识别到：

```text
NVIDIA GeForce RTX 4060 Laptop GPU
Driver Version: 566.26
CUDA Version: 12.7
Memory: 8188 MiB
```

说明 NVIDIA 驱动正常。

### 7.2 检查 PyTorch 是否支持 CUDA

在虚拟环境中执行：

```powershell
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.version.cuda); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NONE')"
```

最初结果是：

```text
torch 2.8.0+cpu
cuda_available False
cuda_version None
gpu_name NONE
```

这说明安装的是 CPU 版 PyTorch，MinerU 只能用 CPU。

### 7.3 安装 CUDA 版 PyTorch

先停止正在运行的 `mineru-api`，然后在虚拟环境中执行：

```powershell
pip uninstall -y torch torchvision torchaudio
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
```

安装完成后再次验证：

```powershell
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.version.cuda); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NONE')"
```

本次结果：

```text
2.11.0+cu126
True
12.6
NVIDIA GeForce RTX 4060 Laptop GPU
```

说明 CUDA 已启用。

注意：本次安装 `torch 2.11.0+cu126` 后出现依赖提示：

```text
lmdeploy 0.11.1 requires torch<=2.8.0,>=2.0.0
lmdeploy 0.11.1 requires torchvision<=0.23.0,>=0.15.0
```

如果只使用 `pipeline` 后端，这个冲突不影响本次测试；如果要使用 `lmdeploy` 后端，建议安装与 `lmdeploy` 兼容的 CUDA 版 PyTorch，例如 `torch==2.8.0`、`torchvision==0.23.0` 对应的 CUDA wheel。

### 7.4 启动 GPU 模式 API

显式指定 MinerU 使用 CUDA：

```powershell
$env:MINERU_DEVICE_MODE="cuda"
mineru-api --host 127.0.0.1 --port 8000
```

再次解析时，日志中出现：

```text
GPU Memory: 8 GB, Batch Ratio: 4.
```

说明 MinerU 已经使用 GPU。之前 CPU 版环境中显示的是：

```text
GPU Memory: 1 GB, Batch Ratio: 1.
```

## 8. 批量转换 demo 目录下四个 PDF

确认 API 健康：

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health | ConvertTo-Json
```

批量转换：

```powershell
mineru -p .\demo\pdfs -o .\output_demo_4pdf -b pipeline --api-url http://127.0.0.1:8000
```

本次处理情况：

```text
4 documents, 37 pages
```

API 端日志显示：

```text
Pipeline processing-window multi-file run. doc_count=4, total_pages=37
Layout Predict: 100%|37/37
MFR Predict: 100%|175/175
Table-ocr det: 100%|16/16
Table-ocr rec ch: 100%|981/981
OCR-det ch: 100%|73/73
OCR-rec Predict: 100%|227/227
Processing pages: 100%|37/37
```

如果客户端中途被中断，但服务端任务已经完成，可以根据任务 ID 查询：

```powershell
Invoke-RestMethod http://127.0.0.1:8000/tasks/7cbf9c89-a575-4416-b098-2488310af159 | ConvertTo-Json -Depth 5
```

返回：

```json
{
  "status": "completed",
  "backend": "pipeline",
  "file_names": ["demo1", "demo3", "small_ocr", "demo2"]
}
```

下载结果：

```powershell
Invoke-WebRequest -Uri http://127.0.0.1:8000/tasks/7cbf9c89-a575-4416-b098-2488310af159/result -OutFile .\output_demo_4pdf_result.zip
Expand-Archive -Path .\output_demo_4pdf_result.zip -DestinationPath .\output_demo_4pdf -Force
```

最终 Markdown 文件：

```text
output_demo_4pdf\demo1\auto\demo1.md
output_demo_4pdf\demo2\auto\demo2.md
output_demo_4pdf\demo3\auto\demo3.md
output_demo_4pdf\small_ocr\auto\small_ocr.md
```

验证文件大小：

```powershell
Get-ChildItem .\output_demo_4pdf -Recurse -Filter *.md | Select-Object Name, DirectoryName, Length | Format-Table -AutoSize
```

示例结果：

```text
demo1.md      51373
demo2.md      32026
demo3.md      46575
small_ocr.md  12713
```

## 9. 将 Markdown 转换为 DOCX

MinerU 原生输出是 Markdown/JSON，不直接输出 DOCX。它支持 DOCX 作为输入，但 PDF 解析结果要得到 Word 文档，推荐流程是：

```text
PDF -> MinerU -> Markdown + images -> Pandoc -> DOCX
```

### 9.1 安装 Pandoc

检查是否安装：

```powershell
pandoc --version
```

如果提示找不到命令，可用 winget 安装：

```powershell
winget install --id JohnMacFarlane.Pandoc -e --accept-package-agreements --accept-source-agreements
```

本次安装后 Pandoc 位于：

```text
C:\Users\zhouh\AppData\Local\Pandoc\pandoc.exe
```

如果当前终端 PATH 尚未刷新，可以直接调用完整路径。

### 9.2 批量转换 DOCX

执行：

```powershell
$pandoc = "$env:LOCALAPPDATA\Pandoc\pandoc.exe"
Get-ChildItem .\output_demo_4pdf -Recurse -Filter *.md | ForEach-Object {
    $docx = Join-Path $_.DirectoryName ($_.BaseName + '.docx')
    $resources = "$($_.DirectoryName);$(Join-Path $_.DirectoryName 'images')"
    & $pandoc $_.FullName -o $docx --resource-path=$resources
}
```

转换过程中 Pandoc 可能对少数公式给出警告：

```text
Could not convert TeX math ... unexpected control sequence \tag
```

这不会阻止 DOCX 生成。相关公式会以 TeX 文本形式保留。

验证 DOCX 输出：

```powershell
Get-ChildItem .\output_demo_4pdf -Recurse -Filter *.docx | Select-Object Name, DirectoryName, Length | Format-Table -AutoSize
```

本次生成结果：

```text
demo1.docx      233284
demo2.docx      217920
demo3.docx      134298
small_ocr.docx   16051
```

输出路径：

```text
output_demo_4pdf\demo1\auto\demo1.docx
output_demo_4pdf\demo2\auto\demo2.docx
output_demo_4pdf\demo3\auto\demo3.docx
output_demo_4pdf\small_ocr\auto\small_ocr.docx
```

## 10. 常见问题总结

### 10.1 访问 `http://127.0.0.1:8000/` 返回 404

正常。MinerU API 没有配置首页。使用下面接口检查：

```powershell
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

### 10.2 第一次运行很慢

正常。首次运行会下载模型，并初始化 OCR、版面、公式、表格等模型。之后模型进入缓存，速度会明显提升。

### 10.3 Windows 提示 Hugging Face 缓存无法使用 symlink

可能出现：

```text
huggingface_hub cache-system uses symlinks by default ... your machine does not support them
```

这是 Windows 权限和开发者模式相关提示，不影响运行，只是缓存占用可能更大。可选择开启 Windows 开发者模式，或以管理员身份运行。

### 10.4 API 任务完成，但客户端输出目录为空

如果 CLI 客户端中途被中断，服务端任务可能仍然完成。用任务 ID 查询：

```powershell
Invoke-RestMethod http://127.0.0.1:8000/tasks/<task_id> | ConvertTo-Json -Depth 5
```

如果 `status` 是 `completed`，下载：

```powershell
Invoke-WebRequest -Uri http://127.0.0.1:8000/tasks/<task_id>/result -OutFile result.zip
Expand-Archive result.zip -DestinationPath output -Force
```

### 10.5 GPU 没有生效

先检查 PyTorch：

```powershell
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.version.cuda)"
```

如果显示 `+cpu` 或 `cuda_available False`，说明当前环境是 CPU 版 PyTorch，需要安装 CUDA 版。

再启动 API 时指定：

```powershell
$env:MINERU_DEVICE_MODE="cuda"
mineru-api --host 127.0.0.1 --port 8000
```

日志中看到 `GPU Memory: 8 GB` 之类的输出，即表示 GPU 生效。

### 10.6 Pandoc 转 DOCX 时公式告警

少数 LaTeX 公式中的 `\tag{}` 可能无法转换为 Word 原生公式。一般不影响 DOCX 文件生成。如果需要完全控制公式样式，可以后续对 Markdown 中的公式做预处理，或在 Word 中人工修订。

## 11. 推荐工作流

最终推荐流程如下：

```powershell
cd E:\MinerU\MinerU
.\.venv\Scripts\Activate.ps1

# 启动 GPU API
$env:MINERU_DEVICE_MODE="cuda"
mineru-api --host 127.0.0.1 --port 8000
```

另开一个终端：

```powershell
cd E:\MinerU\MinerU
.\.venv\Scripts\Activate.ps1

# 批量解析 PDF
mineru -p .\demo\pdfs -o .\output_demo_4pdf -b pipeline --api-url http://127.0.0.1:8000

# 转 DOCX
$pandoc = "$env:LOCALAPPDATA\Pandoc\pandoc.exe"
Get-ChildItem .\output_demo_4pdf -Recurse -Filter *.md | ForEach-Object {
    $docx = Join-Path $_.DirectoryName ($_.BaseName + '.docx')
    $resources = "$($_.DirectoryName);$(Join-Path $_.DirectoryName 'images')"
    & $pandoc $_.FullName -o $docx --resource-path=$resources
}
```

这样即可完成：

```text
PDF -> Markdown/JSON/images -> DOCX
```

## 12. 小结

在 Windows 上运行 MinerU 的关键点是：

1. 使用 Python 3.12，避开 Python 3.13 在 Windows 上的依赖兼容问题。
2. 首次运行先做单文件、单页测试，等待模型下载和初始化完成。
3. 使用 `mineru-api` 作为长期服务，再用 CLI 提交解析任务。
4. GPU 加速依赖 CUDA 版 PyTorch，而不是只看系统是否安装 NVIDIA 驱动。
5. MinerU 原生输出 Markdown/JSON；如需 DOCX，可使用 Pandoc 做二次转换。

本次最终完成了 4 个 PDF、共 37 页的 GPU 加速解析，并成功生成 Markdown、JSON、图片资源和 DOCX 文件。