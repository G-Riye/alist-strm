# alist-strm

本脚本是用来免挂载进行批量创建strm文件供emby、jellyfin等流媒体服务器使用的一个私人化脚本。

## 🎉 新功能 - STRM文件后缀 (v6.0.7)

### 主要特性
- **自定义STRM文件后缀**: 可为每个配置指定不同的STRM文件后缀
- **手动生成功能**: 支持手动为本地视频文件生成STRM文件
- **智能检测**: 系统能够正确检测和验证带后缀的STRM文件
- **向后兼容**: 自动为现有数据库添加新字段，不影响现有功能

### 使用场景
- **Emby转码需求**: 生成带后缀的STRM文件，触发Emby转码而非直放
- **多源管理**: 区分不同来源的STRM文件
- **版本控制**: 管理不同质量版本的STRM文件

脚本使用展示：

![image-20240411060618584](static/images/1.jpg)

![image-20240411063503148](static/images/6c1552959ee5c936a997249e6bebaa2.png)

## 更新日志：

### v6.0.7 (2025-01-15)
- [√] **新增STRM文件后缀功能**
  - 支持自定义STRM文件后缀（默认：-转码）
  - 添加手动生成STRM文件功能
  - 更新验证器以支持带后缀的STRM文件检测
  - 优化用户界面和用户体验

### v6.0.6 (2024-12-20)
- [√] 优化代码结构
- [√] 改进错误处理机制

### v6.0.5 (2024-11-15)
- [√] 新增alist单向同步（即为本地strm文件失效删除）
- [√] 增加复制配置功能
- [√] 增加元数据下载功能
- [√] 支持脚本线程设置
- [√] 元数据格式、视频格式自定义
- [√] webUI增加账户验证

### v6.0.4 (2024-10-08)
- [√] 新增alist签名开启支持（增强alist安全性）
- [√] 部分UI优化操作逻辑
- [√] 定时任务逻辑优化，日志输出优化

### v6.0.3 (2024-09-15)
- [√] 增加配置文件管理webUI管理界面
- [√] 增加定时任务配置
- [√] 支持多线程运行，选择配置文件运行多线程运行
- [√] 优化代码结构
- [√] 弃用.ini方式的配置文件存储方式，更改为轻量级数据库SQLlite

github地址，如果各位大佬觉得脚本好用的可以帮我点个小星星哦。

## 部署

### 方式一：Docker Compose（推荐）

#### 1. 克隆仓库
```bash
git clone https://github.com/G-Riye/alist-strm.git
cd alist-strm
```

#### 2. 使用构建脚本（Windows）
```bash
# 双击运行
build.bat
```

#### 3. 使用构建脚本（Linux/Mac）
```bash
chmod +x build.sh
./build.sh
```

#### 4. 手动构建和运行
```bash
# 构建镜像
docker build -t g-riye/alist-strm:latest .

# 使用docker-compose启动
docker-compose up -d

# 或者使用Unraid专用配置
docker-compose -f docker-compose.unraid.yml up -d
```

### 方式二：Docker命令

#### 命令行版本：
```bash
docker run -d --name alist-strm -p 15000:5000 \
  -v /mnt/user/appdata/alist-strm/config:/config:rw \
  -v /mnt/user/Vedio:/media:rw,shared \
  -v /mnt/user/clouds/strm:/strm:rw,shared \
  g-riye/alist-strm:latest
```

#### docker-compose.yaml配置
```yaml
version: "3.8"
services:
  alist-strm:
    image: g-riye/alist-strm:latest
    container_name: alist-strm
    restart: unless-stopped
    ports:
      - "15000:5000"
    environment:
      - TZ=Asia/Shanghai
      - CONFIG_PATH=/config
    volumes:
      - /mnt/user/appdata/alist-strm/config:/config:rw
      - /mnt/user/Vedio:/media:rw,shared
      - /mnt/user/clouds/strm:/strm:rw,shared
```

### 拉取docker镜像网络原因看这里

如果本地镜像拉取困难的可以前往镜像包下载地址下载后导入：传送门

导入方式就去百度啦 这里就不说啦

## 配置

### 配置格式是什么

运行起来之后他会有个默认配置。如果不会填可以参考默认配置填入配置

### 配置词条解释：

* **监控路径**：即为你要生成的strm的alist的路径。比如说你访问到alist的_路径_是这样的  
`http://192.168.100.166:5244/115/动漫/剧集/` 那么在这一栏你就需要**填写**`/115/动漫/剧集`
* **alist的url**：这里就不用说了吧，就是你访问alist的地址。上面以上面例子为例就是`http://192.168.100.166:5244`
* **目标目录**：字面意思理解的就是生成strm文件的文件夹路径，但是需要注意的是这里填写的是docker容器内部的路径。比如说我想生成在我nas上的`/home/alist-strm/115`的目录下，我docker运行时已经把宿主机的`/home`映射到容器的`/home`上了，那我现在可以直接填写`/home/alist-strm/115`即可。如果不是的话需要注意对应
* **忽略的目录**：这个就随便填即可，但是**不能留空**。如果有不想创建的目录按需填写
* **STRM文件后缀**：生成的STRM文件名将使用此后缀，例如：movie-转码.strm（默认：-转码）
* **令牌获取见下文**
* **alist是否启用签名**：这个选项用于增强一些用户alist是暴露在公网的安全性，但是会对alist负载产生一点影响。没有特殊需求不推荐开启，如果开启了alist后台也应该对应开启。

### `alist`令牌如何获取：

```
进入alist网页端，使用管理员账号密码登陆至后台
点击设置后
	点击其他
就可以看到令牌啦
```

### 关于定时任务

定时任务选择需要进行定时的任务，在corn表达式中添加你想要的间隔时间。不会填写corn的可以参考

```
每个字段的取值范围和允许的特殊字符如下：

秒 (秒 可选，在某些系统或应用中才支持): 0-59
分钟: 0-59
小时: 0-23
日期: 1-31 （注意一些月份没有31日）
月份: 1-12 或 JAN-DEC
星期: 0-6 或 SUN-SAT，其中0和7都代表周日
（对于不包括秒的cron表达式，则从分钟开始）
Cron表达式中的特殊字符含义：

*：代表任何可能的值，例如在分钟字段表示每分钟。
,：用于指定多个值，比如 MON,WED,FRI 表示周一、周三和周五。
-：表示范围，如 1-5 表示1到5之间的所有数字。
/：用于指定间隔频率，如 0/15 在分钟字段表示每15分钟执行一次。
示例
每天凌晨1点执行：0 1 * * *
每周一到周五的上午9:30执行：30 9 * * 1-5
每隔5分钟执行一次：*/5 * * * *
每月1号和15号的下午2点执行：0 14 1,15 * *
如果需要包含秒，表达式变为7个字段，第一个字段表示秒，其余相同，例如：

每隔10秒执行一次：*/10 * * * * *
```

此信息来自于大模型AI。 填入之后只有到你设定的那个时间他才会自动运行 可以看定时任务的日志查看是否运行了

### 关于多线程运行

本脚本先前都是用的单线程多配置文件的方式运行的，如果alist上的资源较多的话可能会造成等待时间过长等等。如果alist是上了cdn或者防火墙的建议将运行本脚本的ip加入白名单以免请求过快触发阈值。

现在是你只要勾选了配置文件并且点击运行（或定时任务设定）它就会自动以每个配置文件为一个线程进行创建strm文件。

### 脚本配置说明

其实这里面的配置都是字面意思

有几个地方说明下：

* **元数据下载**：即为监控目录中有`.nfo、.xml`文件会下载到对应的目录下
* **失效链接检查**：检查本地strm文件是否失效，如果失效删除strm文件并且清空目录（如果目录下没有strm文件就清空文件夹）
* **启用alist强制刷新**：如果启用的话代表着每一次脚本访问监控目录下的子目录它都会刷新一次alist的目录列表（可以理解为alist的网页端点击刷新按钮），这样会导致产生大量对挂载的网盘的api请求，但是会保证每次都是最新的数据。除非有特殊需求，否则不建议开启
* **脚本运行线程数**：这里设置脚本的线程数，字面意思。在遍历目录时会使用，在下载文件时会使用，创建strm文件也会。但是注意不要开太大了。如果3太慢了建议使用5，最好不要超过10。如果你的nas是12代I5那当我没说（bushi）

### 几个常见问题：

* **运行脚本生成的strm不全**。如果挂载的是115网盘，访问alist网页，查看挂载的存储是否返回"访问的网址不安全。。。。"啥啥啥的等等提示，如果是的话 那就是被115防火墙阻断了。  
解决办法： 1、等待防火墙解封ip（cookie）或者更换cookie重新添加存储 2、更新alist版本，将图示变量设置小点，测试设置为2时正常
* **旧版本升级后使用旧数据库报错，首页上不去**  
解决办法：删除原有数据库后重启容器
* **STRM文件后缀不生效**  
解决办法：确认配置中的strm_suffix字段已正确设置，检查数据库连接是否正常，重启应用程序

至此项目完结撒花，如果有bug博客评论留言吧。大概率没有后续版本更新啦。

## 管理命令

### Docker Compose 命令
```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 重新构建并启动
docker-compose up -d --build
```

### Docker 命令
```bash
# 查看容器状态
docker ps -a

# 查看容器日志
docker logs alist-strm

# 进入容器
docker exec -it alist-strm bash

# 停止容器
docker stop alist-strm

# 删除容器
docker rm alist-strm
```

## 许可证

AGPL-3.0 license
