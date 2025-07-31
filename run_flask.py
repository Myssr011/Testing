#!/usr/bin/env python3
"""
Flask Application Runner
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Add paths
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'database'))

from app.flask_app import app

if __name__ == '__main__':
    # Get configuration from environment variables
    host = os.getenv('APP_HOST', '0.0.0.0')
    port = int(os.getenv('APP_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"Starting Flask app on {host}:{port}")
    print(f"Debug mode: {debug}")
    print(f"Database: {os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}")
    
    app.run(host=host, port=port, debug=debug)
