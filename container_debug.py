#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Docker容器环境调试脚本
专门用于诊断容器中的运行问题
"""

import os
import sys
import time
import psutil
import requests
import easywebdav
from datetime import datetime
from db_handler import DBHandler
from logger import setup_logger

def check_container_environment():
    """检查容器环境"""
    print("🔍 Docker容器环境检查")
    print("=" * 60)
    
    # 检查是否在容器中
    is_docker = os.path.exists('/.dockerenv')
    print(f"是否在Docker容器中: {is_docker}")
    
    # 检查关键目录
    key_dirs = ['/app', '/app/logs', '/app/cache', '/config', '/data']
    for dir_path in key_dirs:
        if os.path.exists(dir_path):
            try:
                stat = os.stat(dir_path)
                print(f"✅ {dir_path}: 存在 (权限: {oct(stat.st_mode)[-3:]})")
            except Exception as e:
                print(f"❌ {dir_path}: 存在但权限检查失败: {e}")
        else:
            print(f"❌ {dir_path}: 不存在")
    
    # 检查系统资源
    print(f"\n💻 系统资源:")
    print(f"  CPU核心数: {psutil.cpu_count()}")
    print(f"  内存总量: {psutil.virtual_memory().total / 1024 / 1024 / 1024:.1f} GB")
    print(f"  可用内存: {psutil.virtual_memory().available / 1024 / 1024 / 1024:.1f} GB")
    
    # 检查网络连接
    print(f"\n🌐 网络连接测试:")
    try:
        response = requests.get('http://www.baidu.com', timeout=10)
        print(f"  外网连接: ✅ (状态码: {response.status_code})")
    except Exception as e:
        print(f"  外网连接: ❌ ({e})")

def test_webdav_connection(config_id):
    """测试WebDAV连接"""
    print(f"\n🔗 WebDAV连接测试 (配置ID: {config_id})")
    print("=" * 60)
    
    try:
        db = DBHandler()
        db.initialize_tables()
        config = db.get_webdav_config(config_id)
        
        if not config:
            print(f"❌ 未找到配置ID: {config_id}")
            return False
        
        print(f"配置信息:")
        print(f"  名称: {config['config_name']}")
        print(f"  地址: {config['protocol']}://{config['host']}:{config['port']}")
        print(f"  根路径: {config['rootpath']}")
        print(f"  目标目录: {config['target_directory']}")
        
        # 测试连接
        print(f"\n正在测试WebDAV连接...")
        start_time = time.time()
        
        webdav = easywebdav.connect(
            host=config['host'],
            port=config['port'],
            username=config['username'],
            password=config['password'],
            protocol=config['protocol']
        )
        
        # 测试列出根目录
        files = webdav.ls('/')
        end_time = time.time()
        
        print(f"✅ WebDAV连接成功!")
        print(f"  连接耗时: {end_time - start_time:.2f} 秒")
        print(f"  根目录文件数: {len(files)}")
        
        # 测试列出配置的根路径
        print(f"\n正在测试根路径: {config['rootpath']}")
        try:
            root_files = webdav.ls(config['rootpath'])
            print(f"✅ 根路径访问成功!")
            print(f"  文件数: {len(root_files)}")
            
            # 显示前几个文件
            for i, f in enumerate(root_files[:5]):
                print(f"  {i+1}. {f.name} ({f.size} bytes)")
            if len(root_files) > 5:
                print(f"  ... 还有 {len(root_files) - 5} 个文件")
                
        except Exception as e:
            print(f"❌ 根路径访问失败: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ WebDAV连接失败: {e}")
        return False

def test_file_operations(config_id):
    """测试文件操作"""
    print(f"\n📁 文件操作测试")
    print("=" * 60)
    
    try:
        db = DBHandler()
        config = db.get_webdav_config(config_id)
        
        if not config:
            print(f"❌ 未找到配置ID: {config_id}")
            return False
        
        target_dir = config['target_directory']
        
        # 检查目标目录
        if not os.path.exists(target_dir):
            print(f"创建目标目录: {target_dir}")
            os.makedirs(target_dir, exist_ok=True)
        
        # 测试写入权限
        test_file = os.path.join(target_dir, 'test_write.txt')
        try:
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write('测试写入权限')
            print(f"✅ 文件写入测试成功: {test_file}")
            
            # 测试删除
            os.remove(test_file)
            print(f"✅ 文件删除测试成功")
            
        except Exception as e:
            print(f"❌ 文件操作测试失败: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 文件操作测试失败: {e}")
        return False

def monitor_process_execution(config_id, duration=60):
    """监控进程执行"""
    print(f"\n📈 进程执行监控 (持续{duration}秒)")
    print("=" * 60)
    
    # 启动main.py进程
    import subprocess
    
    command = f"python main.py {config_id}"
    print(f"启动命令: {command}")
    
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print(f"进程已启动，PID: {process.pid}")
        print(f"开始监控...")
        
        start_time = time.time()
        last_output_time = start_time
        
        while time.time() - start_time < duration:
            # 检查进程是否还在运行
            if process.poll() is not None:
                print(f"❌ 进程已退出，返回码: {process.returncode}")
                break
            
            # 检查进程状态
            try:
                proc = psutil.Process(process.pid)
                cpu_percent = proc.cpu_percent()
                memory_info = proc.memory_info()
                
                current_time = time.time()
                if current_time - last_output_time >= 5:  # 每5秒输出一次状态
                    print(f"⏰ {datetime.now().strftime('%H:%M:%S')} - "
                          f"CPU: {cpu_percent:.1f}%, "
                          f"内存: {memory_info.rss / 1024 / 1024:.1f}MB, "
                          f"状态: {proc.status()}")
                    last_output_time = current_time
                
            except psutil.NoSuchProcess:
                print(f"❌ 进程不存在")
                break
            
            time.sleep(1)
        
        # 如果进程还在运行，强制终止
        if process.poll() is None:
            print(f"⏰ 监控时间结束，终止进程")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        
        # 获取输出
        stdout, stderr = process.communicate()
        if stdout:
            print(f"\n📤 标准输出:")
            print(stdout[-1000:])  # 只显示最后1000字符
        if stderr:
            print(f"\n📤 错误输出:")
            print(stderr[-1000:])  # 只显示最后1000字符
            
    except Exception as e:
        print(f"❌ 启动进程失败: {e}")

def main():
    if len(sys.argv) < 2:
        print("用法: python container_debug.py <config_id> [monitor_duration]")
        return
    
    config_id = int(sys.argv[1])
    monitor_duration = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    
    print(f"🔧 Docker容器调试工具")
    print(f"配置ID: {config_id}")
    print(f"监控时长: {monitor_duration}秒")
    print("=" * 60)
    
    # 1. 检查容器环境
    check_container_environment()
    
    # 2. 测试WebDAV连接
    if not test_webdav_connection(config_id):
        print(f"\n❌ WebDAV连接测试失败，停止后续测试")
        return
    
    # 3. 测试文件操作
    if not test_file_operations(config_id):
        print(f"\n❌ 文件操作测试失败，停止后续测试")
        return
    
    # 4. 监控进程执行
    monitor_process_execution(config_id, monitor_duration)
    
    print(f"\n✅ 调试完成")

if __name__ == "__main__":
    main()
