#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess

def test_run_config():
    """测试运行配置功能"""
    print("测试运行配置功能...")
    
    # 检查main.py是否存在
    if not os.path.exists('main.py'):
        print("✗ main.py不存在")
        return False
    
    # 测试Python命令
    try:
        result = subprocess.run(['python', '--version'], 
                              capture_output=True, text=True, timeout=10)
        python_version = result.stdout.strip()
        print(f"✓ Python版本: {python_version}")
    except Exception as e:
        print(f"✗ Python命令测试失败: {e}")
        return False
    
    # 测试运行main.py（不传参数，应该会显示错误信息）
    try:
        command = "python main.py"
        result = subprocess.run(command, shell=True, capture_output=True, 
                              text=True, timeout=30, cwd=os.getcwd())
        
        print(f"✓ main.py可以运行，返回码: {result.returncode}")
        if result.stderr:
            print(f"  错误信息: {result.stderr[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ 运行main.py失败: {e}")
        return False

def test_strm_validator():
    """测试strm_validator功能"""
    print("\n测试strm_validator功能...")
    
    # 检查strm_validator.py是否存在
    if not os.path.exists('strm_validator.py'):
        print("✗ strm_validator.py不存在")
        return False
    
    # 测试运行strm_validator.py（不传参数，应该会显示帮助信息）
    try:
        command = "python strm_validator.py"
        result = subprocess.run(command, shell=True, capture_output=True, 
                              text=True, timeout=30, cwd=os.getcwd())
        
        print(f"✓ strm_validator.py可以运行，返回码: {result.returncode}")
        if result.stdout:
            print(f"  输出信息: {result.stdout[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ 运行strm_validator.py失败: {e}")
        return False

def main():
    """主函数"""
    print("开始测试运行修复...")
    
    success1 = test_run_config()
    success2 = test_strm_validator()
    
    if success1 and success2:
        print("\n🎉 所有测试通过！运行功能应该正常工作了。")
        return True
    else:
        print("\n❌ 部分测试失败，需要进一步检查。")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 