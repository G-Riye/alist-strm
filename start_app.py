#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

def start_app():
    """Start the Flask application"""
    print("🚀 Starting Alist STRM Generator...")
    print("📱 Access at: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the application")
    print("-" * 50)

    # Set environment variable
    os.environ['FLASK_DEBUG'] = 'False'  # Disable debug mode

    # Import and start the application
    from app import app
    app.run(host="0.0.0.0", port=5000, debug=False)

if __name__ == '__main__':
    start_app()
