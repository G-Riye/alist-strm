#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import importlib.util

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python version {version.major}.{version.minor} is too old. Please use Python 3.8+")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def install_requirements():
    """Install requirements"""
    print("\n📦 Installing requirements...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    directories = ['logs', 'cache', 'invalid_file_trees']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"✅ Directory exists: {directory}")

def test_db_handler():
    """Test db_handler module"""
    print("\n🗄️ Testing db_handler...")
    try:
        from db_handler import DBHandler
        db = DBHandler()
        print("✅ db_handler imported successfully")
        return True
    except Exception as e:
        print(f"❌ db_handler test failed: {e}")
        return False

def test_main_script():
    """Test main.py script"""
    print("\n📄 Testing main.py...")
    try:
        # Test if main.py can be imported
        spec = importlib.util.spec_from_file_location("main", "main.py")
        main_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main_module)
        print("✅ main.py imported successfully")
        return True
    except Exception as e:
        print(f"❌ main.py test failed: {e}")
        return False

def start_app():
    """Start the Flask application"""
    print("\n🚀 Starting Flask application...")
    print("📱 Access at: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the application")
    print("-" * 50)
    
    # Set environment variable to disable debug mode
    os.environ['FLASK_DEBUG'] = 'False'
    
    try:
        from app import app
        app.run(host="0.0.0.0", port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Failed to start application: {e}")

def main():
    """Main function"""
    print("🔧 Setting up local development environment...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install requirements
    if not install_requirements():
        return
    
    # Create directories
    create_directories()
    
    # Initialize database
    print("\n🔧 Initializing database...")
    try:
        from init_db import init_database, test_database
        init_database()
        test_database()
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return
    
    # Test modules
    if not test_db_handler():
        return
    
    if not test_main_script():
        return
    
    print("\n✅ All checks passed!")
    
    # Ask user if they want to start the app
    response = input("\n🚀 Do you want to start the Flask application? (y/n): ")
    if response.lower() in ['y', 'yes', '是']:
        start_app()
    else:
        print("👋 Setup complete. You can start the app manually with: python app.py")

if __name__ == '__main__':
    main()
