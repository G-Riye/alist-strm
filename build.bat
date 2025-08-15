@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: 颜色定义
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

:: 版本号和镜像名
set "VERSION=6.0.7"
set "IMAGE_NAME=g-riye/alist-strm"

echo %BLUE%=== alist-strm Docker 构建脚本 ===%NC%
echo %YELLOW%版本: %VERSION%%NC%
echo %YELLOW%镜像名: %IMAGE_NAME%%NC%
echo.

:: 检查Docker是否运行
docker info >nul 2>&1
if errorlevel 1 (
    echo %RED%错误: Docker 未运行或未安装%NC%
    pause
    exit /b 1
)

:: 构建镜像
echo %BLUE%开始构建 Docker 镜像...%NC%
docker build -t %IMAGE_NAME%:latest .
docker build -t %IMAGE_NAME%:%VERSION% .

if errorlevel 1 (
    echo %RED%✗ Docker 镜像构建失败！%NC%
    pause
    exit /b 1
) else (
    echo %GREEN%✓ Docker 镜像构建成功！%NC%
)

:: 询问是否推送到Docker Hub
echo.
set /p "PUSH_CHOICE=是否推送到 Docker Hub? (y/n): "
if /i "!PUSH_CHOICE!"=="y" (
    echo %BLUE%推送镜像到 Docker Hub...%NC%
    docker push %IMAGE_NAME%:latest
    docker push %IMAGE_NAME%:%VERSION%
    
    if errorlevel 1 (
        echo %RED%✗ 镜像推送失败！%NC%
    ) else (
        echo %GREEN%✓ 镜像推送成功！%NC%
        echo %GREEN%镜像地址: https://hub.docker.com/r/%IMAGE_NAME%%NC%
    )
)

:: 询问是否运行容器
echo.
set /p "RUN_CHOICE=是否立即运行容器? (y/n): "
if /i "!RUN_CHOICE!"=="y" (
    echo %BLUE%启动容器...%NC%
    docker-compose up -d
    
    if errorlevel 1 (
        echo %RED%✗ 容器启动失败！%NC%
    ) else (
        echo %GREEN%✓ 容器启动成功！%NC%
        echo %GREEN%访问地址: http://localhost:15000%NC%
    )
)

echo.
echo %GREEN%=== 构建完成 ===%NC%
echo %YELLOW%使用以下命令管理容器:%NC%
echo   启动: %BLUE%docker-compose up -d%NC%
echo   停止: %BLUE%docker-compose down%NC%
echo   查看日志: %BLUE%docker-compose logs -f%NC%
echo   重启: %BLUE%docker-compose restart%NC%

pause
