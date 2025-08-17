#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
下载功能调试脚本
用于检查下载队列和下载功能的状态
"""

import sys
import os
from db_handler import DBHandler
from logger import setup_logger

def debug_download_status(config_id):
    """调试下载功能状态"""
    print(f"🔍 下载功能调试 (配置ID: {config_id})")
    print("=" * 60)
    
    try:
        # 获取配置
        db = DBHandler()
        db.initialize_tables()
        config = db.get_webdav_config(config_id)
        
        if not config:
            print(f"❌ 未找到配置ID: {config_id}")
            return
        
        print(f"配置信息:")
        print(f"  名称: {config['config_name']}")
        print(f"  目标目录: {config['target_directory']}")
        print(f"  下载功能: {'启用' if config.get('download_enabled', 1) == 1 else '禁用'}")
        print(f"  下载间隔: {config.get('download_interval_range', '未设置')}")
        
        # 检查目标目录
        target_dir = config['target_directory']
        if os.path.exists(target_dir):
            print(f"✅ 目标目录存在: {target_dir}")
            
            # 列出目标目录中的文件
            files = os.listdir(target_dir)
            print(f"  目录中的文件数量: {len(files)}")
            if files:
                print(f"  前5个文件:")
                for i, file in enumerate(files[:5]):
                    print(f"    {i+1}. {file}")
                if len(files) > 5:
                    print(f"    ... 还有 {len(files) - 5} 个文件")
        else:
            print(f"❌ 目标目录不存在: {target_dir}")
        
        # 检查日志文件
        log_file = f"logs/config_{config_id}.log"
        if os.path.exists(log_file):
            print(f"\n📋 日志文件分析: {log_file}")
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                print(f"  总行数: {len(lines)}")
                
                # 查找关键信息
                download_lines = [line for line in lines if '下载' in line]
                queue_lines = [line for line in lines if '队列' in line]
                total_lines = [line for line in lines if '总共需要下载' in line]
                completed_lines = [line for line in lines if '总共下载了' in line]
                
                print(f"  包含'下载'的行数: {len(download_lines)}")
                print(f"  包含'队列'的行数: {len(queue_lines)}")
                print(f"  包含'总共需要下载'的行数: {len(total_lines)}")
                print(f"  包含'总共下载了'的行数: {len(completed_lines)}")
                
                # 显示最后10行日志
                if lines:
                    print(f"\n  最后10行日志:")
                    for line in lines[-10:]:
                        print(f"    {line.strip()}")
                
                # 显示下载相关的日志
                if download_lines:
                    print(f"\n  下载相关日志 (最后5条):")
                    for line in download_lines[-5:]:
                        print(f"    {line.strip()}")
                
            except Exception as e:
                print(f"❌ 读取日志文件失败: {e}")
        else:
            print(f"❌ 日志文件不存在: {log_file}")
        
        # 检查缓存文件
        cache_file = f"cache/webdav_directory_cache_{config_id}.json"
        if os.path.exists(cache_file):
            print(f"\n📁 缓存文件存在: {cache_file}")
            try:
                import json
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                print(f"  缓存文件大小: {len(cache_data)} 个项目")
            except Exception as e:
                print(f"❌ 读取缓存文件失败: {e}")
        else:
            print(f"❌ 缓存文件不存在: {cache_file}")
        
    except Exception as e:
        print(f"❌ 调试失败: {e}")

def check_download_queue():
    """检查下载队列状态"""
    print(f"\n🔍 下载队列状态检查")
    print("=" * 60)
    
    try:
        # 这里我们需要模拟检查下载队列的状态
        # 由于队列是全局变量，我们需要通过日志来推断
        
        # 检查是否有正在运行的Python进程
        import psutil
        python_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'python' in proc.name().lower():
                    cmdline = proc.cmdline()
                    if cmdline and 'main.py' in ' '.join(cmdline):
                        python_processes.append({
                            'pid': proc.pid,
                            'cmdline': ' '.join(cmdline),
                            'status': proc.status()
                        })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if python_processes:
            print(f"找到 {len(python_processes)} 个运行中的main.py进程:")
            for proc in python_processes:
                print(f"  PID: {proc['pid']}, 状态: {proc['status']}")
                print(f"  命令: {proc['cmdline']}")
        else:
            print("未找到运行中的main.py进程")
        
    except Exception as e:
        print(f"❌ 检查进程状态失败: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python debug_download.py <config_id>")
        sys.exit(1)
    
    config_id = int(sys.argv[1])
    
    debug_download_status(config_id)
    check_download_queue()
    
    print(f"\n✅ 调试完成")
