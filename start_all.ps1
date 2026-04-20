# 街舞信息共享平台一键启动脚本
# 作用：
# 1. 在独立窗口启动 Django 后端，后端脚本会自动执行 migrate、seed_demo_data 和 runserver。
# 2. 在独立窗口启动 React + Vite 前端，方便浏览器访问 http://127.0.0.1:5173。
# 3. 启动前先检查关键文件，避免路径错误时窗口一闪而过、不方便定位问题。

$ErrorActionPreference = "Stop"

# 始终以脚本所在目录作为项目根目录，避免用户从其他目录运行时找不到文件。
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendScript = Join-Path $ProjectRoot "start_backend.ps1"
$FrontendScript = Join-Path $ProjectRoot "start_frontend.ps1"
$VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$FrontendDir = Join-Path $ProjectRoot "frontend"
$PackageJson = Join-Path $FrontendDir "package.json"
$NodeModules = Join-Path $FrontendDir "node_modules"

Write-Host "正在检查街舞信息共享平台启动环境..." -ForegroundColor Cyan

# 后端必须使用项目本地虚拟环境，避免误用系统 Python。
if (-not (Test-Path $VenvPython)) {
    Write-Host "未找到项目本地 Python：$VenvPython" -ForegroundColor Red
    Write-Host "请先创建 .venv 并安装 requirements.txt 中的后端依赖。" -ForegroundColor Yellow
    Read-Host "按回车键退出"
    exit 1
}

if (-not (Test-Path $BackendScript)) {
    Write-Host "未找到后端启动脚本：$BackendScript" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

if (-not (Test-Path $FrontendScript)) {
    Write-Host "未找到前端启动脚本：$FrontendScript" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

if (-not (Test-Path $PackageJson)) {
    Write-Host "未找到前端 package.json：$PackageJson" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

# 如果前端依赖缺失，给出明确提示；不在这里自动安装，避免演示时等待过久或网络失败。
if (-not (Test-Path $NodeModules)) {
    Write-Host "提示：未检测到 frontend\node_modules，请先进入 frontend 执行 npm install。" -ForegroundColor Yellow
}

Write-Host "检查完成，正在分别启动后端和前端..." -ForegroundColor Green

# 后端窗口保持独立，方便查看迁移、演示数据和 Django 服务日志。
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-ExecutionPolicy", "Bypass",
    "-File", "`"$BackendScript`""
) -WorkingDirectory $ProjectRoot

# 前端窗口保持独立，方便查看 Vite dev server 地址和编译日志。
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-ExecutionPolicy", "Bypass",
    "-File", "`"$FrontendScript`""
) -WorkingDirectory $ProjectRoot

Write-Host ""
Write-Host "启动命令已发出：" -ForegroundColor Cyan
Write-Host "后端地址：http://127.0.0.1:8000"
Write-Host "前端地址：http://127.0.0.1:5173"
Write-Host ""
Write-Host "如果浏览器暂时打不开，请等待两个窗口中的服务启动完成。" -ForegroundColor Yellow
