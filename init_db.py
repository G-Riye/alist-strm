#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3
import shutil

def init_database():
    """Initialize the database"""
    print("🔧 Initializing database...")

    # Use config.db in the current directory
    db_file = 'config.db'

    # If test_config.db exists, copy it
    if os.path.exists('test_config.db'):
        shutil.copy2('test_config.db', db_file)
        print(f"✅ Copied test_config.db to {db_file}")

    # Connect to the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create config table
    cursor.execute('''CREATE TABLE IF NOT EXISTS config (
        config_id INTEGER PRIMARY KEY AUTOINCREMENT,
        config_name TEXT,
        url TEXT,
        username TEXT,
        password TEXT,
        rootpath TEXT,
        target_directory TEXT,
        download_enabled INTEGER DEFAULT 1,
        update_mode TEXT DEFAULT 'incremental',
        download_interval_range TEXT DEFAULT '1-3',
        strm_suffix TEXT DEFAULT '-转码'
    )''')

    # Create user_config table
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_config (
        video_formats TEXT DEFAULT 'mp4,mkv,avi,mov,flv,wmv,ts,m2ts',
        subtitle_formats TEXT DEFAULT 'srt,ass,sub',
        image_formats TEXT DEFAULT 'jpg,png,bmp',
        metadata_formats TEXT DEFAULT 'nfo',
        size_threshold INTEGER DEFAULT 100,
        username TEXT,
        password TEXT
    )''')

    # Insert default configuration
    cursor.execute("SELECT COUNT(*) FROM user_config")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''INSERT INTO user_config
            (video_formats, subtitle_formats, image_formats, metadata_formats, size_threshold)
            VALUES (?, ?, ?, ?, ?)''',
            ('mp4,mkv,avi,mov,flv,wmv,ts,m2ts', 'srt,ass,sub', 'jpg,png,bmp', 'nfo', 100))
        print("✅ Inserted default user configuration")

    # Check for config data
    cursor.execute("SELECT COUNT(*) FROM config")
    config_count = cursor.fetchone()[0]
    print(f"✅ Database has {config_count} configurations")

    conn.commit()
    conn.close()

    print(f"✅ Database initialization complete: {db_file}")
    return db_file

def test_database():
    """Test database connection"""
    print("\n🧪 Testing database connection...")

    try:
        from db_handler import DBHandler
        db = DBHandler()

        # Test query
        configs = db.cursor.execute("SELECT config_id, config_name FROM config").fetchall()
        print(f"✅ Database connection successful, found {len(configs)} configurations")

        for config_id, config_name in configs:
            print(f"   - ID: {config_id}, Name: {config_name}")

        return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

if __name__ == '__main__':
    # Initialize database
    db_file = init_database()

    # Test database
    test_database()

    print("\n🎉 Database initialization complete!")
