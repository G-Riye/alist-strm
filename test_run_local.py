#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import time
from db_handler import DBHandler

def test_run_local():
    """Test run_config and strm_validator locally"""
    print("🧪 Testing run_config and strm_validator locally...")
    print("=" * 50)
    
    # Get config from database
    try:
        db = DBHandler()
        configs = db.cursor.execute("SELECT config_id, config_name FROM config").fetchall()
        
        if not configs:
            print("❌ No configurations found in database")
            return
        
        print(f"✅ Found {len(configs)} configurations:")
        for config_id, config_name in configs:
            print(f"   - ID: {config_id}, Name: {config_name}")
        
        # Use first config for testing
        config_id = configs[0][0]
        config_name = configs[0][1]
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return
    
    # Test run_config (main.py)
    print(f"\n🚀 Testing run_config (main.py) with config ID: {config_id}")
    try:
        # Run main.py in background
        command = f"python main.py {config_id}"
        print(f"Executing: {command}")
        
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print(f"✅ Process started with PID: {process.pid}")
        
        # Wait a bit for log file to be created
        time.sleep(3)
        
        # Check if log file was created
        log_files = [f for f in os.listdir('logs') if f.startswith(f'config_{config_id}')]
        if log_files:
            print(f"✅ Log file created: {log_files[0]}")
            
            # Read log content
            log_path = os.path.join('logs', log_files[0])
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"📝 Log content (last 10 lines):")
                lines = content.strip().split('\n')
                for line in lines[-10:]:
                    print(f"   {line}")
        else:
            print("❌ No log file created")
        
        # Wait for process to complete
        print("⏳ Waiting for process to complete...")
        process.wait(timeout=60)
        
        if process.returncode == 0:
            print("✅ main.py completed successfully")
        else:
            print(f"❌ main.py failed with return code: {process.returncode}")
            
    except subprocess.TimeoutExpired:
        print("⏰ Process timed out (60 seconds)")
        process.kill()
    except Exception as e:
        print(f"❌ Error running main.py: {e}")
    
    # Test strm_validator
    print(f"\n🔍 Testing strm_validator with config ID: {config_id}")
    try:
        command = f"python strm_validator.py {config_id} quick"
        print(f"Executing: {command}")
        
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(f"Return code: {result.returncode}")
        if result.stdout:
            print(f"Output:\n{result.stdout}")
        if result.stderr:
            print(f"Error:\n{result.stderr}")
            
        if result.returncode == 0:
            print("✅ strm_validator completed successfully")
        else:
            print("❌ strm_validator failed")
            
    except subprocess.TimeoutExpired:
        print("⏰ strm_validator timed out")
    except Exception as e:
        print(f"❌ Error running strm_validator: {e}")
    
    print("\n🎉 Local testing complete!")

if __name__ == '__main__':
    test_run_local()
