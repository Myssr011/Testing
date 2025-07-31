#!/usr/bin/env python3
"""
Script untuk menambahkan data sample dan admin user
"""

import sys
import os
from datetime import datetime, date
import bcrypt

# Add src path untuk import modules
sys.path.append(os.path.join(os.path.dirname(__file__)))

from migrate_app import app, db, User, Abstract, SimilarityResult, DetectionBatch, SystemLog


def create_admin_user():
    """Create default admin user"""
    try:
        with app.app_context():
            # Check if admin user already exists
            admin = User.query.filter_by(username='admin').first()
            if admin:
                print("✅ Admin user already exists")
                return True
            
            # Hash password
            password = 'admin123'
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Create admin user
            admin = User(
                username='admin',
                email='admin@plagiarismchecker.com',
                password_hash=password_hash,
                role='admin',
                is_active=True
            )
            
            db.session.add(admin)
            db.session.commit()
            
            print("✅ Admin user created successfully")
            print("   Username: admin")
            print("   Password: admin123")
            print("   Email: admin@plagiarismchecker.com")
            return True
            
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.session.rollback()
        return False


def create_sample_users():
    """Create sample users"""
    try:
        with app.app_context():
            sample_users = [
                {
                    'username': 'reviewer1',
                    'email': 'reviewer1@unismuh.ac.id',
                    'password': 'reviewer123',
                    'role': 'reviewer'
                },
                {
                    'username': 'user1',
                    'email': 'mahasiswa1@unismuh.ac.id',
                    'password': 'user123',
                    'role': 'user'
                },
                {
                    'username': 'user2',
                    'email': 'mahasiswa2@unismuh.ac.id',
                    'password': 'user123',
                    'role': 'user'
                }
            ]
            
            for user_data in sample_users:
                # Check if user already exists
                existing_user = User.query.filter_by(username=user_data['username']).first()
                if existing_user:
                    print(f"✅ User {user_data['username']} already exists")
                    continue
                
                # Hash password
                password_hash = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                # Create user
                user = User(
                    username=user_data['username'],
                    email=user_data['email'],
                    password_hash=password_hash,
                    role=user_data['role'],
                    is_active=True
                )
                
                db.session.add(user)
                print(f"✅ Created user: {user_data['username']}")
            
            db.session.commit()
            return True
            
    except Exception as e:
        print(f"❌ Error creating sample users: {e}")
        db.session.rollback()
        return False


def create_sample_abstracts():
    """Create sample abstracts"""
    try:
        with app.app_context():
            # Get a user to assign as uploader
            user = User.query.filter_by(username='user1').first()
            if not user:
                print("❌ User not found for sample abstracts")
                return False
            
            sample_abstracts = [
                {
                    'title': 'Implementasi Algoritma Machine Learning untuk Prediksi Cuaca',
                    'author': 'Ahmad Fauzi',
                    'institution': 'Universitas Muhammadiyah Makassar',
                    'year': 2024,
                    'abstract_text': 'Penelitian ini mengimplementasikan algoritma machine learning untuk prediksi cuaca. Metode yang digunakan adalah Random Forest dan Support Vector Machine. Hasil penelitian menunjukkan akurasi prediksi mencapai 85% untuk data cuaca di Kota Makassar.',
                    'file_type': 'pdf',
                    'language': 'id',
                    'upload_date': date.today(),
                    'uploaded_by': user.id
                },
                {
                    'title': 'Analisis Kinerja Sistem Informasi Manajemen Akademik',
                    'author': 'Siti Nurhaliza',
                    'institution': 'Universitas Muhammadiyah Makassar',
                    'year': 2024,
                    'abstract_text': 'Sistem informasi manajemen akademik merupakan bagian penting dalam pengelolaan data akademik. Penelitian ini menganalisis kinerja sistem dengan menggunakan metrik response time dan throughput. Hasil analisis menunjukkan perlunya optimalisasi database untuk meningkatkan performa.',
                    'file_type': 'docx',
                    'language': 'id',
                    'upload_date': date.today(),
                    'uploaded_by': user.id
                },
                {
                    'title': 'Penerapan Internet of Things dalam Smart Home System',
                    'author': 'Muhammad Rizki',
                    'institution': 'Universitas Muhammadiyah Makassar',
                    'year': 2023,
                    'abstract_text': 'Internet of Things (IoT) telah menjadi teknologi yang berkembang pesat. Penelitian ini menerapkan konsep IoT untuk membangun smart home system. Sistem yang dikembangkan dapat mengontrol lampu, AC, dan keamanan rumah secara otomatis menggunakan sensor dan smartphone.',
                    'file_type': 'pdf',
                    'language': 'id',
                    'upload_date': date.today(),
                    'uploaded_by': user.id
                }
            ]
            
            for abstract_data in sample_abstracts:
                # Check if abstract already exists
                existing_abstract = Abstract.query.filter_by(title=abstract_data['title']).first()
                if existing_abstract:
                    print(f"✅ Abstract '{abstract_data['title'][:50]}...' already exists")
                    continue
                
                # Create abstract
                abstract = Abstract(**abstract_data)
                db.session.add(abstract)
                print(f"✅ Created abstract: {abstract_data['title'][:50]}...")
            
            db.session.commit()
            return True
            
    except Exception as e:
        print(f"❌ Error creating sample abstracts: {e}")
        db.session.rollback()
        return False


def create_sample_system_log():
    """Create sample system log"""
    try:
        with app.app_context():
            # Get admin user
            admin = User.query.filter_by(username='admin').first()
            
            log_entry = SystemLog(
                log_level='INFO',
                module='database',
                message='Database initialized successfully',
                details={'action': 'database_setup', 'version': '1.0'},
                user_id=admin.id if admin else None,
                ip_address='127.0.0.1',
                user_agent='Setup Script'
            )
            
            db.session.add(log_entry)
            db.session.commit()
            
            print("✅ Sample system log created")
            return True
            
    except Exception as e:
        print(f"❌ Error creating system log: {e}")
        db.session.rollback()
        return False


def main():
    """Main function to run all setup tasks"""
    print("🚀 SETTING UP PLAGIARISM DETECTION SYSTEM DATABASE")
    print("=" * 60)
    
    success = True
    
    # Create admin user
    print("\n📊 Creating admin user...")
    if not create_admin_user():
        success = False
    
    # Create sample users
    print("\n👥 Creating sample users...")
    if not create_sample_users():
        success = False
    
    # Create sample abstracts
    print("\n📄 Creating sample abstracts...")
    if not create_sample_abstracts():
        success = False
    
    # Create sample system log
    print("\n📝 Creating sample system log...")
    if not create_sample_system_log():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("✅ DATABASE SETUP COMPLETED SUCCESSFULLY!")
        print("\n📋 Summary:")
        
        with app.app_context():
            user_count = User.query.count()
            abstract_count = Abstract.query.count()
            log_count = SystemLog.query.count()
            
            print(f"   - Users: {user_count}")
            print(f"   - Abstracts: {abstract_count}")
            print(f"   - System Logs: {log_count}")
            
        print("\n🔐 Admin Login:")
        print("   Username: admin")
        print("   Password: admin123")
        
    else:
        print("❌ SETUP COMPLETED WITH ERRORS!")
        print("   Please check the error messages above.")


if __name__ == '__main__':
    main()
