#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
进程诊断脚本
用于分析Python进程的运行状态和问题
"""

import psutil
import time
import os
from datetime import datetime

def diagnose_python_processes():
    """诊断Python进程状态"""
    print("🔍 Python进程诊断报告")
    print("=" * 60)
    print(f"诊断时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    python_processes = []
    
    # 查找所有Python进程
    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_percent', 'create_time', 'status']):
        try:
            proc_info = proc.info
            
            # 检查是否是Python进程
            if proc_info['name'] and 'python' in proc_info['name'].lower():
                # 获取更详细的进程信息
                proc_info['cpu_percent'] = proc.cpu_percent()
                proc_info['memory_percent'] = proc.memory_percent()
                proc_info['memory_info'] = proc.memory_info()
                proc_info['num_threads'] = proc.num_threads()
                proc_info['num_fds'] = proc.num_fds() if hasattr(proc, 'num_fds') else 'N/A'
                
                python_processes.append(proc_info)
                
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    
    if not python_processes:
        print("❌ 未找到Python进程")
        return
    
    print(f"📊 找到 {len(python_processes)} 个Python进程:")
    print()
    
    for i, proc in enumerate(python_processes, 1):
        print(f"进程 {i}:")
        print(f"  PID: {proc['pid']}")
        print(f"  名称: {proc['name']}")
        print(f"  命令行: {' '.join(proc['cmdline']) if proc['cmdline'] else 'N/A'}")
        print(f"  状态: {proc['status']}")
        print(f"  CPU使用率: {proc['cpu_percent']:.1f}%")
        print(f"  内存使用率: {proc['memory_percent']:.1f}%")
        print(f"  内存使用: {proc['memory_info'].rss / 1024 / 1024:.1f} MB")
        print(f"  线程数: {proc['num_threads']}")
        print(f"  文件描述符: {proc['num_fds']}")
        print(f"  启动时间: {datetime.fromtimestamp(proc['create_time']).strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 检查是否是我们的应用进程
        cmdline_str = ' '.join(proc['cmdline']) if proc['cmdline'] else ''
        if 'main.py' in cmdline_str or 'app.py' in cmdline_str:
            print(f"  🎯 这是我们的应用进程!")
            
            # 检查进程是否在等待
            if proc['status'] == 'sleeping' and proc['cpu_percent'] == 0:
                print(f"  ⚠️  进程处于sleep状态且CPU使用率为0，可能存在问题")
                
                # 检查进程是否在等待I/O
                try:
                    proc_obj = psutil.Process(proc['pid'])
                    io_counters = proc_obj.io_counters()
                    print(f"  📊 I/O统计: 读取={io_counters.read_bytes/1024:.1f}KB, 写入={io_counters.write_bytes/1024:.1f}KB")
                except:
                    print(f"  📊 I/O统计: 无法获取")
        
        print("-" * 40)
    
    # 系统资源使用情况
    print("\n🖥️  系统资源使用情况:")
    print(f"  CPU使用率: {psutil.cpu_percent(interval=1)}%")
    memory = psutil.virtual_memory()
    print(f"  内存使用率: {memory.percent}%")
    print(f"  可用内存: {memory.available / 1024 / 1024 / 1024:.1f} GB")
    
    # 检查关键目录
    print("\n📁 关键目录检查:")
    key_dirs = ['/app', '/app/logs', '/app/cache', '/config', '/data']
    for dir_path in key_dirs:
        if os.path.exists(dir_path):
            try:
                stat = os.stat(dir_path)
                print(f"  {dir_path}: 存在 (权限: {oct(stat.st_mode)[-3:]})")
            except Exception as e:
                print(f"  {dir_path}: 存在 (权限检查失败: {e})")
        else:
            print(f"  {dir_path}: 不存在")

def monitor_process_realtime(pid=None, duration=30):
    """实时监控进程状态"""
    print(f"\n📈 实时进程监控 (持续{duration}秒)")
    print("=" * 60)
    
    if pid:
        try:
            proc = psutil.Process(pid)
            print(f"监控进程 PID: {pid}")
        except psutil.NoSuchProcess:
            print(f"❌ 进程 {pid} 不存在")
            return
    else:
        # 找到第一个Python进程
        python_procs = [p for p in psutil.process_iter(['pid', 'name']) 
                       if p.info['name'] and 'python' in p.info['name'].lower()]
        if not python_procs:
            print("❌ 未找到Python进程")
            return
        proc = psutil.Process(python_procs[0].info['pid'])
        print(f"监控第一个Python进程 PID: {proc.pid}")
    
    start_time = time.time()
    print(f"{'时间':<12} {'CPU%':<8} {'内存%':<8} {'状态':<10} {'线程':<6} {'I/O读取':<10} {'I/O写入':<10}")
    print("-" * 80)
    
    while time.time() - start_time < duration:
        try:
            cpu_percent = proc.cpu_percent()
            memory_percent = proc.memory_percent()
            status = proc.status()
            num_threads = proc.num_threads()
            
            try:
                io_counters = proc.io_counters()
                io_read = f"{io_counters.read_bytes/1024:.1f}KB"
                io_write = f"{io_counters.write_bytes/1024:.1f}KB"
            except:
                io_read = "N/A"
                io_write = "N/A"
            
            current_time = datetime.now().strftime('%H:%M:%S')
            print(f"{current_time:<12} {cpu_percent:<8.1f} {memory_percent:<8.1f} {status:<10} {num_threads:<6} {io_read:<10} {io_write:<10}")
            
            time.sleep(2)
            
        except psutil.NoSuchProcess:
            print(f"❌ 进程 {proc.pid} 已终止")
            break
        except Exception as e:
            print(f"❌ 监控出错: {e}")
            break

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "monitor" and len(sys.argv) > 2:
            # 实时监控指定进程
            try:
                pid = int(sys.argv[2])
                duration = int(sys.argv[3]) if len(sys.argv) > 3 else 30
                monitor_process_realtime(pid, duration)
            except ValueError:
                print("❌ 无效的PID或持续时间")
        else:
            print("用法: python diagnose_process.py [monitor <pid> [duration]]")
    else:
        # 默认诊断
        diagnose_python_processes()
        
        # 询问是否要实时监控
        print("\n" + "=" * 60)
        print("💡 提示:")
        print("1. 如果进程显示为sleep状态，可能是正常的等待状态")
        print("2. 如果CPU使用率为0且长时间无变化，可能存在问题")
        print("3. 使用 'python diagnose_process.py monitor <pid> [duration]' 进行实时监控")
        print("4. 检查日志文件了解程序的具体运行情况")
