#!/bin/bash

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 版本号
VERSION="6.0.7"
IMAGE_NAME="g-riye/alist-strm"

echo -e "${BLUE}=== alist-strm Docker 构建脚本 ===${NC}"
echo -e "${YELLOW}版本: ${VERSION}${NC}"
echo -e "${YELLOW}镜像名: ${IMAGE_NAME}${NC}"
echo ""

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}错误: Docker 未运行或未安装${NC}"
    exit 1
fi

# 构建镜像
echo -e "${BLUE}开始构建 Docker 镜像...${NC}"
docker build -t ${IMAGE_NAME}:latest .
docker build -t ${IMAGE_NAME}:${VERSION} .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Docker 镜像构建成功！${NC}"
else
    echo -e "${RED}✗ Docker 镜像构建失败！${NC}"
    exit 1
fi

# 询问是否推送到Docker Hub
echo ""
read -p "是否推送到 Docker Hub? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}推送镜像到 Docker Hub...${NC}"
    docker push ${IMAGE_NAME}:latest
    docker push ${IMAGE_NAME}:${VERSION}
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ 镜像推送成功！${NC}"
        echo -e "${GREEN}镜像地址: https://hub.docker.com/r/${IMAGE_NAME}${NC}"
    else
        echo -e "${RED}✗ 镜像推送失败！${NC}"
        exit 1
    fi
fi

# 询问是否运行容器
echo ""
read -p "是否立即运行容器? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}启动容器...${NC}"
    docker-compose up -d
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ 容器启动成功！${NC}"
        echo -e "${GREEN}访问地址: http://localhost:15000${NC}"
    else
        echo -e "${RED}✗ 容器启动失败！${NC}"
        exit 1
    fi
fi

echo ""
echo -e "${GREEN}=== 构建完成 ===${NC}"
echo -e "${YELLOW}使用以下命令管理容器:${NC}"
echo -e "  启动: ${BLUE}docker-compose up -d${NC}"
echo -e "  停止: ${BLUE}docker-compose down${NC}"
echo -e "  查看日志: ${BLUE}docker-compose logs -f${NC}"
echo -e "  重启: ${BLUE}docker-compose restart${NC}"
