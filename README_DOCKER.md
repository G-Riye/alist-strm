# Alist STRM Generator - Docker 使用指南

## 🐳 Docker 镜像信息

- **镜像名称**: `riye/alist-strm`
- **最新版本**: `v6.0.7`
- **支持架构**: `linux/amd64`, `linux/arm64`

## 📋 功能特性

- ✅ **STRM文件生成**: 自动为视频文件生成STRM文件
- ✅ **自定义后缀**: 支持自定义STRM文件后缀（如 `-转码`）
- ✅ **增量更新**: 支持增量更新，只处理新增文件
- ✅ **批量处理**: 支持批量生成STRM文件
- ✅ **Web界面**: 提供友好的Web管理界面
- ✅ **定时任务**: 支持定时任务调度
- ✅ **日志管理**: 完整的日志记录和查看功能

## 🚀 快速开始

### 1. 拉取镜像
```bash
docker pull riye/alist-strm:latest
```

### 2. 运行容器
```bash
docker run -d \
  --name alist-strm \
  -p 5000:5000 \
  -v /path/to/config:/config \
  -v /path/to/media:/media \
  riye/alist-strm:latest
```

### 3. 访问Web界面
打开浏览器访问: `http://localhost:5000`

## 📁 目录映射

| 容器路径 | 宿主机路径 | 说明 |
|---------|-----------|------|
| `/config` | `/path/to/config` | 配置文件目录 |
| `/media` | `/path/to/media` | 媒体文件目录 |

## ⚙️ 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `WEB_PORT` | `5000` | Web服务端口 |
| `SECURITY_CODE` | `alist-strm` | 安全码 |

### 使用环境变量运行
```bash
docker run -d \
  --name alist-strm \
  -p 8080:8080 \
  -e WEB_PORT=8080 \
  -e SECURITY_CODE=my-secret \
  -v /config:/config \
  -v /media:/media \
  riye/alist-strm:latest
```

## 🐳 Docker Compose

创建 `docker-compose.yml` 文件：

```yaml
version: '3.8'

services:
  alist-strm:
    image: riye/alist-strm:latest
    container_name: alist-strm
    ports:
      - "5000:5000"
    volumes:
      - ./config:/config
      - ./media:/media
    environment:
      - WEB_PORT=5000
      - SECURITY_CODE=alist-strm
    restart: unless-stopped
```

运行：
```bash
docker-compose up -d
```

## 🔧 配置说明

### 1. 首次访问
- 访问 `http://localhost:5000`
- 注册管理员账户
- 配置WebDAV连接信息

### 2. 配置WebDAV
- **URL**: Alist服务器地址
- **用户名**: Alist用户名
- **密码**: Alist密码
- **根路径**: WebDAV根路径
- **目标目录**: 本地媒体文件目录
- **STRM后缀**: 自定义STRM文件后缀（如 `-转码`）

### 3. 运行配置
- 点击"运行"按钮开始生成STRM文件
- 查看日志了解处理进度
- 支持增量更新和全量更新

## 📊 版本历史

### v6.0.7 (最新)
- 🆕 新增STRM文件后缀功能
- 🆕 支持自定义STRM文件后缀
- 🆕 添加手动生成STRM文件功能
- 🐛 修复日志查看500错误
- 🐛 修复运行配置功能问题
- 🐛 修复Python脚本运行问题

### v6.0.6
- 🆕 基础STRM文件生成功能
- 🆕 Web管理界面
- 🆕 定时任务支持

## 🔍 故障排除

### 1. 容器无法启动
```bash
# 查看容器日志
docker logs alist-strm

# 检查端口占用
netstat -tlnp | grep 5000
```

### 2. Web界面无法访问
- 检查端口映射是否正确
- 确认防火墙设置
- 查看容器状态：`docker ps`

### 3. STRM文件未生成
- 检查WebDAV配置是否正确
- 查看应用日志
- 确认目标目录权限

## 📞 支持

- **GitHub**: [https://github.com/riye/alist-strm](https://github.com/riye/alist-strm)
- **Issues**: [https://github.com/riye/alist-strm/issues](https://github.com/riye/alist-strm/issues)

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件 