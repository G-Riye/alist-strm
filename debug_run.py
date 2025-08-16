#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import json
from db_handler import DBHandler

def debug_environment():
    """调试环境信息"""
    print("=== 环境信息 ===")
    print(f"Python版本: {sys.version}")
    print(f"当前工作目录: {os.getcwd()}")
    print(f"Python可执行文件: {sys.executable}")
    
    # 检查关键文件是否存在
    key_files = ['main.py', 'strm_validator.py', 'db_handler.py', 'logger.py']
    print("\n=== 文件检查 ===")
    for file in key_files:
        exists = os.path.exists(file)
        print(f"{file}: {'✓' if exists else '✗'}")
        if exists:
            size = os.path.getsize(file)
            print(f"  大小: {size} 字节")
    
    # 检查logs目录
    logs_dir = 'logs'
    if os.path.exists(logs_dir):
        print(f"\nlogs目录: ✓")
        log_files = os.listdir(logs_dir)
        print(f"日志文件数量: {len(log_files)}")
        for log_file in log_files[:5]:  # 只显示前5个
            print(f"  - {log_file}")
    else:
        print(f"\nlogs目录: ✗ (不存在)")

def debug_database():
    """调试数据库连接"""
    print("\n=== 数据库检查 ===")
    try:
        db = DBHandler()
        db.initialize_tables()
        print("数据库连接: ✓")
        
        # 检查配置
        configs = db.cursor.execute("SELECT config_id, config_name FROM config").fetchall()
        print(f"配置数量: {len(configs)}")
        for config in configs:
            print(f"  - ID: {config[0]}, 名称: {config[1]}")
            
    except Exception as e:
        print(f"数据库连接: ✗ - {e}")

def debug_python_command():
    """调试Python命令"""
    print("\n=== Python命令测试 ===")
    
    # 测试python命令
    try:
        result = subprocess.run(['python', '--version'], 
                              capture_output=True, text=True, timeout=10)
        print(f"python --version: {result.stdout.strip()}")
    except Exception as e:
        print(f"python --version: ✗ - {e}")
    
    # 测试python3命令
    try:
        result = subprocess.run(['python3', '--version'], 
                              capture_output=True, text=True, timeout=10)
        print(f"python3 --version: {result.stdout.strip()}")
    except Exception as e:
        print(f"python3 --version: ✗ - {e}")

def test_main_script(config_id=1):
    """测试main.py脚本"""
    print(f"\n=== 测试main.py脚本 (config_id={config_id}) ===")
    
    if not os.path.exists('main.py'):
        print("main.py不存在")
        return
    
    try:
        # 测试导入
        print("测试导入...")
        import main
        print("导入main.py: ✓")
        
        # 测试运行
        print("测试运行...")
        command = f"python main.py {config_id}"
        result = subprocess.run(command, shell=True, capture_output=True, 
                              text=True, timeout=60, cwd=os.getcwd())
        
        print(f"返回码: {result.returncode}")
        if result.stdout:
            print(f"标准输出: {result.stdout[:500]}...")
        if result.stderr:
            print(f"错误输出: {result.stderr[:500]}...")
            
    except Exception as e:
        print(f"测试失败: {e}")

def test_strm_validator(config_id=1):
    """测试strm_validator.py脚本"""
    print(f"\n=== 测试strm_validator.py脚本 (config_id={config_id}) ===")
    
    if not os.path.exists('strm_validator.py'):
        print("strm_validator.py不存在")
        return
    
    try:
        # 测试导入
        print("测试导入...")
        import strm_validator
        print("导入strm_validator.py: ✓")
        
        # 测试运行
        print("测试运行...")
        command = f"python strm_validator.py {config_id} quick"
        result = subprocess.run(command, shell=True, capture_output=True, 
                              text=True, timeout=60, cwd=os.getcwd())
        
        print(f"返回码: {result.returncode}")
        if result.stdout:
            print(f"标准输出: {result.stdout[:500]}...")
        if result.stderr:
            print(f"错误输出: {result.stderr[:500]}...")
            
    except Exception as e:
        print(f"测试失败: {e}")

def main():
    """主函数"""
    print("开始调试运行问题...")
    
    debug_environment()
    debug_database()
    debug_python_command()
    
    # 获取第一个配置ID进行测试
    try:
        db = DBHandler()
        configs = db.cursor.execute("SELECT config_id FROM config LIMIT 1").fetchall()
        if configs:
            config_id = configs[0][0]
            test_main_script(config_id)
            test_strm_validator(config_id)
        else:
            print("\n没有找到配置，跳过脚本测试")
    except Exception as e:
        print(f"\n无法获取配置: {e}")
    
    print("\n=== 调试完成 ===")

if __name__ == '__main__':
    main() 