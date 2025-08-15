# STRM文件后缀功能说明

## 功能概述

本功能允许用户为生成的STRM文件指定自定义后缀，以便区分不同类型的STRM文件。这对于需要同时维护原始STRM文件和转码用STRM文件的场景特别有用。

## 主要特性

1. **自定义后缀**: 可以为每个配置指定不同的STRM文件后缀
2. **默认后缀**: 默认使用"-转码"作为后缀
3. **独立生成**: 可以单独为本地视频文件生成带后缀的STRM文件
4. **智能检测**: 系统能够正确检测和验证带后缀的STRM文件

## 使用方法

### 1. 配置STRM后缀

在创建或编辑配置时，可以设置"STRM文件后缀"字段：

- **默认值**: `-转码`
- **示例**: 
  - `-转码` → 生成 `movie-转码.strm`
  - `-alist` → 生成 `movie-alist.strm`
  - `-remote` → 生成 `movie-remote.strm`

### 2. 生成STRM文件

有两种方式生成带后缀的STRM文件：

#### 方式一：通过主程序自动生成
- 运行配置时，系统会自动为符合条件的视频文件生成带后缀的STRM文件
- 生成的文件名格式：`{原文件名}{后缀}.strm`

#### 方式二：手动生成
- 在配置列表页面，点击对应配置的"生成STRM"按钮
- 系统会扫描本地视频文件并为它们生成STRM文件

### 3. 验证STRM文件

使用STRM验证器可以检测和验证带后缀的STRM文件：

```bash
# 快速扫描
python strm_validator.py <config_id> quick

# 慢速扫描
python strm_validator.py <config_id> slow

# 生成STRM文件
python strm_validator.py <config_id> generate
```

## 技术实现

### 数据库变更

在`config`表中添加了新字段：
```sql
ALTER TABLE config ADD COLUMN strm_suffix TEXT DEFAULT '-转码';
```

### 代码修改

1. **db_handler.py**: 添加了strm_suffix字段的支持
2. **main.py**: 修改了create_strm_file函数以支持自定义后缀
3. **strm_validator.py**: 更新了检测和生成逻辑
4. **app.py**: 添加了生成STRM文件的路由
5. **模板文件**: 更新了配置表单以包含后缀设置

### 文件命名规则

- **原始STRM文件**: `movie.strm`
- **带后缀STRM文件**: `movie-转码.strm`
- **支持任意后缀**: 用户可以根据需要自定义

## 使用场景

### 场景一：Emby转码需求
- 原始文件：`movie.mp4`
- 原始STRM：`movie.strm` (直放)
- 转码STRM：`movie-转码.strm` (转码)

### 场景二：多源管理
- 本地源：`movie-local.strm`
- 远程源：`movie-remote.strm`
- 备用源：`movie-backup.strm`

### 场景三：版本控制
- 高清版：`movie-hd.strm`
- 标清版：`movie-sd.strm`
- 压缩版：`movie-compressed.strm`

## 注意事项

1. **文件冲突**: 确保不同配置使用不同的后缀，避免文件名冲突
2. **路径一致性**: 生成的STRM文件路径需要与原始视频文件路径保持一致
3. **权限设置**: 生成的STRM文件会自动设置777权限
4. **大小阈值**: 只有超过设定大小阈值的视频文件才会生成STRM文件

## 故障排除

### 常见问题

1. **STRM文件未生成**
   - 检查视频文件大小是否超过阈值
   - 确认视频格式是否在支持列表中
   - 验证目标目录权限

2. **后缀不生效**
   - 确认配置中的strm_suffix字段已正确设置
   - 检查数据库连接是否正常
   - 重启应用程序

3. **验证失败**
   - 检查网络连接
   - 验证Alist服务是否正常运行
   - 确认用户名密码是否正确

### 日志查看

可以通过以下方式查看详细日志：
- 在Web界面查看配置日志
- 检查应用程序日志文件
- 使用STRM验证器的详细输出模式

## 更新历史

- **v6.0.6**: 添加STRM文件后缀功能
  - 支持自定义STRM文件后缀
  - 添加手动生成STRM文件功能
  - 更新验证器以支持带后缀的STRM文件
  - 优化用户界面和用户体验
