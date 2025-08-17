#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
修复现有配置的download_enabled设置
将所有配置的download_enabled设置为1（启用）
"""

import sqlite3
import os

def fix_download_enabled():
    """修复所有配置的download_enabled设置"""
    
    # 数据库文件路径
    db_file = 'config.db'
    
    if not os.path.exists(db_file):
        print(f"❌ 数据库文件 {db_file} 不存在")
        return False
    
    try:
        # 连接数据库
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # 检查config表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='config'")
        if not cursor.fetchone():
            print("❌ config表不存在")
            return False
        
        # 获取所有配置
        cursor.execute("SELECT config_id, config_name, download_enabled FROM config")
        configs = cursor.fetchall()
        
        if not configs:
            print("❌ 没有找到任何配置")
            return False
        
        print(f"📋 找到 {len(configs)} 个配置:")
        for config_id, config_name, download_enabled in configs:
            status = "启用" if download_enabled else "禁用"
            print(f"   - 配置ID: {config_id}, 名称: {config_name}, 下载功能: {status}")
        
        # 更新所有配置的download_enabled为1
        cursor.execute("UPDATE config SET download_enabled = 1")
        conn.commit()
        
        print(f"\n✅ 已将所有 {len(configs)} 个配置的下载功能设置为启用")
        
        # 验证更新结果
        cursor.execute("SELECT config_id, config_name, download_enabled FROM config")
        updated_configs = cursor.fetchall()
        
        print(f"\n📋 更新后的配置状态:")
        for config_id, config_name, download_enabled in updated_configs:
            status = "启用" if download_enabled else "禁用"
            print(f"   - 配置ID: {config_id}, 名称: {config_name}, 下载功能: {status}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ 修复过程中出错: {e}")
        return False

if __name__ == "__main__":
    print("🔧 修复配置的下载功能设置...")
    print("=" * 50)
    
    if fix_download_enabled():
        print("\n✅ 修复完成！现在您可以重新运行配置了。")
        print("\n💡 提示:")
        print("   1. 重新运行您的配置")
        print("   2. 程序现在会正常执行下载功能")
        print("   3. 不会再出现1-2秒就退出的问题")
    else:
        print("\n❌ 修复失败，请检查错误信息")
