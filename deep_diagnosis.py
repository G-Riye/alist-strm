#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
深度诊断脚本
专门用于分析程序在容器中提前停止的原因
"""

import os
import sys
import time
import signal
import psutil
import subprocess
import threading
from datetime import datetime
from db_handler import DBHandler
from logger import setup_logger

def monitor_system_resources(duration=60):
    """监控系统资源使用情况"""
    print(f"📊 系统资源监控 (持续{duration}秒)")
    print("=" * 60)
    
    start_time = time.time()
    data_points = []
    
    while time.time() - start_time < duration:
        try:
            # CPU使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # 内存使用情况
            memory = psutil.virtual_memory()
            
            # 磁盘使用情况
            disk = psutil.disk_usage('/')
            
            # 网络连接数
            net_connections = len(psutil.net_connections())
            
            # 文件描述符数量
            try:
                with open('/proc/sys/fs/file-nr', 'r') as f:
                    file_nr = f.read().strip().split()
                    open_files = int(file_nr[0])
            except:
                open_files = 0
            
            data_point = {
                'timestamp': time.time(),
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available': memory.available / 1024 / 1024 / 1024,  # GB
                'disk_percent': disk.percent,
                'net_connections': net_connections,
                'open_files': open_files
            }
            
            data_points.append(data_point)
            
            print(f"⏰ {datetime.now().strftime('%H:%M:%S')} - "
                  f"CPU: {cpu_percent:.1f}%, "
                  f"内存: {memory.percent:.1f}% ({memory.available / 1024 / 1024 / 1024:.1f}GB可用), "
                  f"磁盘: {disk.percent:.1f}%, "
                  f"网络连接: {net_connections}, "
                  f"文件描述符: {open_files}")
            
        except Exception as e:
            print(f"❌ 监控错误: {e}")
            break
    
    # 分析数据
    if data_points:
        print(f"\n📈 资源使用分析:")
        cpu_values = [d['cpu_percent'] for d in data_points]
        memory_values = [d['memory_percent'] for d in data_points]
        
        print(f"  CPU使用率: 平均 {sum(cpu_values)/len(cpu_values):.1f}%, 最高 {max(cpu_values):.1f}%")
        print(f"  内存使用率: 平均 {sum(memory_values)/len(memory_values):.1f}%, 最高 {max(memory_values):.1f}%")
        
        # 检查是否有资源瓶颈
        if max(cpu_values) > 80:
            print(f"  ⚠️  CPU使用率过高，可能导致进程被限制")
        if max(memory_values) > 80:
            print(f"  ⚠️  内存使用率过高，可能导致OOM killer")
    
    return data_points

def run_with_monitoring(config_id, duration=120):
    """运行程序并监控"""
    print(f"🚀 运行程序监控 (配置ID: {config_id}, 持续{duration}秒)")
    print("=" * 60)
    
    # 启动main.py进程
    command = f"python main.py {config_id}"
    print(f"启动命令: {command}")
    
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=os.setsid  # 创建新的进程组
        )
        
        print(f"进程已启动，PID: {process.pid}")
        print(f"进程组ID: {os.getpgid(process.pid)}")
        
        start_time = time.time()
        last_output_time = start_time
        output_buffer = []
        
        # 监控进程状态
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
                          f"PID: {process.pid}, "
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
            try:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                time.sleep(2)
                if process.poll() is None:
                    os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            except Exception as e:
                print(f"终止进程时出错: {e}")
        
        # 获取输出
        stdout, stderr = process.communicate()
        
        print(f"\n📤 程序输出分析:")
        if stdout:
            print(f"标准输出 (最后500字符):")
            print(stdout[-500:])
        if stderr:
            print(f"错误输出 (最后500字符):")
            print(stderr[-500:])
        
        # 分析日志文件
        analyze_logs(config_id)
        
    except Exception as e:
        print(f"❌ 启动进程失败: {e}")

def analyze_logs(config_id):
    """分析日志文件"""
    print(f"\n📋 日志文件分析")
    print("=" * 60)
    
    log_file = f"logs/config_{config_id}.log"
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            print(f"日志文件: {log_file}")
            print(f"总行数: {len(lines)}")
            
            if lines:
                print(f"最后10行日志:")
                for line in lines[-10:]:
                    print(f"  {line.strip()}")
                
                # 查找关键信息
                error_lines = [line for line in lines if 'ERROR' in line or 'Exception' in line]
                if error_lines:
                    print(f"\n⚠️  发现错误信息:")
                    for line in error_lines[-5:]:  # 显示最后5个错误
                        print(f"  {line.strip()}")
                
                # 查找程序退出信息
                exit_lines = [line for line in lines if '退出' in line or 'exit' in line.lower()]
                if exit_lines:
                    print(f"\n🚪 程序退出信息:")
                    for line in exit_lines:
                        print(f"  {line.strip()}")
            
        except Exception as e:
            print(f"❌ 读取日志文件失败: {e}")
    else:
        print(f"❌ 日志文件不存在: {log_file}")

def check_container_limits():
    """检查容器限制"""
    print(f"🔒 容器限制检查")
    print("=" * 60)
    
    # 检查CPU限制
    try:
        with open('/sys/fs/cgroup/cpu/cpu.cfs_quota_us', 'r') as f:
            cpu_quota = int(f.read().strip())
        with open('/sys/fs/cgroup/cpu/cpu.cfs_period_us', 'r') as f:
            cpu_period = int(f.read().strip())
        
        if cpu_quota > 0:
            cpu_limit = cpu_quota / cpu_period
            print(f"CPU限制: {cpu_limit} 核心")
        else:
            print(f"CPU限制: 无限制")
    except Exception as e:
        print(f"CPU限制检查失败: {e}")
    
    # 检查内存限制
    try:
        with open('/sys/fs/cgroup/memory/memory.limit_in_bytes', 'r') as f:
            memory_limit = int(f.read().strip())
        
        if memory_limit > 0:
            memory_limit_gb = memory_limit / 1024 / 1024 / 1024
            print(f"内存限制: {memory_limit_gb:.1f} GB")
        else:
            print(f"内存限制: 无限制")
    except Exception as e:
        print(f"内存限制检查失败: {e}")
    
    # 检查文件描述符限制
    try:
        import resource
        soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        print(f"文件描述符限制: 软限制 {soft}, 硬限制 {hard}")
    except Exception as e:
        print(f"文件描述符限制检查失败: {e}")

def main():
    if len(sys.argv) < 2:
        print("用法: python deep_diagnosis.py <config_id> [duration]")
        return
    
    config_id = int(sys.argv[1])
    duration = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    
    print(f"🔬 深度诊断工具")
    print(f"配置ID: {config_id}")
    print(f"诊断时长: {duration}秒")
    print("=" * 60)
    
    # 1. 检查容器限制
    check_container_limits()
    
    # 2. 监控系统资源
    print(f"\n开始系统资源监控...")
    resource_data = monitor_system_resources(30)  # 先监控30秒
    
    # 3. 运行程序并监控
    run_with_monitoring(config_id, duration)
    
    print(f"\n✅ 深度诊断完成")

if __name__ == "__main__":
    main()
