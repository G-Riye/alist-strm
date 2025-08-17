#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单的WebDAV连接测试脚本
"""

import sys
import time
import requests
import easywebdav
from db_handler import DBHandler

def test_webdav_simple(config_id):
    """简单测试WebDAV连接"""
    print(f"🔗 简单WebDAV连接测试 (配置ID: {config_id})")
    print("=" * 60)
    
    try:
        # 获取配置
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
        
        # 测试HTTP连接
        print(f"\n🌐 测试HTTP连接...")
        try:
            url = f"{config['protocol']}://{config['host']}:{config['port']}"
            response = requests.get(url, timeout=10)
            print(f"✅ HTTP连接成功: {response.status_code}")
        except Exception as e:
            print(f"❌ HTTP连接失败: {e}")
            return False
        
        # 测试WebDAV连接
        print(f"\n🔗 测试WebDAV连接...")
        try:
            webdav = easywebdav.connect(
                host=config['host'],
                port=config['port'],
                username=config['username'],
                password=config['password'],
                protocol=config['protocol']
            )
            print(f"✅ WebDAV连接创建成功")
            
            # 直接测试配置的根路径，跳过根目录测试
            print(f"📁 测试根路径: {config['rootpath']}")
            try:
                root_files = webdav.ls(config['rootpath'])
                print(f"✅ 根路径访问成功，文件数: {len(root_files)}")
                
                # 显示前几个文件
                for i, f in enumerate(root_files[:3]):
                    print(f"  {i+1}. {f.name} ({f.size} bytes)")
                if len(root_files) > 3:
                    print(f"  ... 还有 {len(root_files) - 3} 个文件")
                
                return True
                
            except Exception as e:
                print(f"❌ 根路径访问失败: {e}")
                return False
            
        except Exception as e:
            print(f"❌ WebDAV连接失败: {e}")
            return False
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_network_connectivity():
    """测试网络连接"""
    print(f"🌐 网络连接测试")
    print("=" * 60)
    
    # 测试DNS解析
    try:
        import socket
        host = "openlist.469510353.xyz"
        ip = socket.gethostbyname(host)
        print(f"✅ DNS解析成功: {host} -> {ip}")
    except Exception as e:
        print(f"❌ DNS解析失败: {e}")
    
    # 测试HTTP连接
    try:
        response = requests.get("https://openlist.469510353.xyz:8443", timeout=10)
        print(f"✅ HTTPS连接成功: {response.status_code}")
    except Exception as e:
        print(f"❌ HTTPS连接失败: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python test_webdav_simple.py <config_id>")
        sys.exit(1)
    
    config_id = int(sys.argv[1])
    
    print(f"🔧 简单WebDAV测试工具")
    print(f"配置ID: {config_id}")
    print("=" * 60)
    
    # 1. 测试网络连接
    test_network_connectivity()
    
    # 2. 测试WebDAV连接
    if test_webdav_simple(config_id):
        print(f"\n✅ 所有测试通过！")
    else:
        print(f"\n❌ 测试失败！")
