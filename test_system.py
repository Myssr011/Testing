#!/usr/bin/env python3
"""
Simple Database and System Test
Test koneksi database dan komponen sistem utama
"""
import os
import sys
import socket
from pathlib import Path

def load_env():
    """Load environment variables from .env file"""
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
        print("✅ Environment variables loaded from .env")
    else:
        print("⚠️  .env file not found, using default values")

def test_database_connection():
    """Test database network connection"""
    host = os.getenv('DB_HOST', 'localhost')
    port = int(os.getenv('DB_PORT', 3306))
    
    print(f"\n🔌 Testing database connection to {host}:{port}")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print("✅ Database server is reachable")
            return True
        else:
            print("❌ Cannot connect to database server")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_python_imports():
    """Test if required Python packages can be imported"""
    print("\n📦 Testing Python package imports...")
    
    packages = {
        'flask': 'Flask',
        'sqlalchemy': 'SQLAlchemy',
        'sklearn': 'scikit-learn',
        'nltk': 'NLTK',
        'pandas': 'Pandas',
        'PyMySQL': 'PyMySQL'
    }
    
    results = {}
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"✅ {name} - OK")
            results[package] = True
        except ImportError:
            print(f"❌ {name} - Not installed")
            results[package] = False
    
    return results

def test_file_structure():
    """Test if required files and directories exist"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        'app/flask_app.py',
        'src/preprocessing.py',
        'src/vectorizer.py',
        'src/similarity.py',
        'database/models.py',
        'requirements.txt'
    ]
    
    required_dirs = [
        'app/templates',
        'app/static',
        'uploads',
        'results'
    ]
    
    all_exist = True
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - Missing")
            all_exist = False
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/ - Missing")
            all_exist = False
    
    return all_exist

def test_flask_app():
    """Test if Flask app can be imported"""
    print("\n🌐 Testing Flask application...")
    
    try:
        sys.path.append('app')
        import flask_app
        print("✅ Flask application can be imported")
        return True
    except Exception as e:
        print(f"❌ Flask application error: {e}")
        return False

def run_simple_database_test():
    """Run simple database test if packages are available"""
    print("\n🧪 Running database functionality test...")
    
    try:
        import pymysql
        
        host = os.getenv('DB_HOST')
        port = int(os.getenv('DB_PORT', 3306))
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        database = os.getenv('DB_NAME')
        
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            connect_timeout=10
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ Database connection successful - MySQL {version[0]}")
        
        connection.close()
        return True
        
    except ImportError:
        print("⚠️  PyMySQL not available, skipping database test")
        return None
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 PLAGIARISM DETECTION SYSTEM - QUICK TEST")
    print("=" * 50)
    
    # Load environment
    load_env()
    
    # Run tests
    results = {
        'network': test_database_connection(),
        'imports': all(test_python_imports().values()),
        'files': test_file_structure(),
        'flask': test_flask_app(),
        'database': run_simple_database_test()
    }
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    for test_name, result in results.items():
        if result is True:
            print(f"✅ {test_name.upper()}: PASSED")
        elif result is False:
            print(f"❌ {test_name.upper()}: FAILED")
        else:
            print(f"⚠️  {test_name.upper()}: SKIPPED")
    
    # Overall result
    passed_tests = [r for r in results.values() if r is True]
    failed_tests = [r for r in results.values() if r is False]
    
    print(f"\nResults: {len(passed_tests)} passed, {len(failed_tests)} failed")
    
    if len(failed_tests) == 0:
        print("\n🎉 All tests passed! System is ready to use.")
        return 0
    elif len(passed_tests) > len(failed_tests):
        print("\n⚠️  Some tests failed but system should be functional.")
        print("   Check the failed tests and install missing dependencies.")
        return 1
    else:
        print("\n❌ Multiple tests failed. Please fix the issues before proceeding.")
        print("\nTroubleshooting:")
        print("1. Run: pip install -r requirements.txt")
        print("2. Check .env file configuration")
        print("3. Ensure database server is running")
        return 2

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
