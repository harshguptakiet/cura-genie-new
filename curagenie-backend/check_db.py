#!/usr/bin/env python3

import sqlite3
import sys
from db.database import engine, get_db
from db.auth_models import User, PatientProfile
from sqlalchemy.orm import Session

def check_database():
    """Check database tables and create test user"""
    print("🔍 Checking CuraGenie Database...")
    
    # Check SQLite tables
    try:
        conn = sqlite3.connect('curagenie.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"📋 Tables found: {tables}")
        
        # Check users table specifically
        if 'users' in tables:
            cursor.execute("SELECT COUNT(*) FROM users;")
            user_count = cursor.fetchone()[0]
            print(f"👥 Users in database: {user_count}")
            
            if user_count > 0:
                cursor.execute("SELECT id, email, username, role FROM users LIMIT 5;")
                users = cursor.fetchall()
                print("📄 Sample users:")
                for user in users:
                    print(f"   - ID: {user[0]}, Email: {user[1]}, Username: {user[2]}, Role: {user[3]}")
        else:
            print("❌ Users table not found!")
            
        conn.close()
    except Exception as e:
        print(f"❌ Database error: {e}")
    
    # Test with SQLAlchemy
    print("\n🔧 Testing SQLAlchemy connection...")
    try:
        db = next(get_db())
        users = db.query(User).all()
        print(f"✅ SQLAlchemy found {len(users)} users")
        db.close()
    except Exception as e:
        print(f"❌ SQLAlchemy error: {e}")

def create_test_user():
    """Create a test user for login testing"""
    print("\n👤 Creating test user...")
    
    try:
        from core.auth import get_password_hash
        
        db = next(get_db())
        
        # Check if test user already exists
        existing_user = db.query(User).filter(User.email == "test@test.com").first()
        if existing_user:
            print("✅ Test user already exists: test@test.com")
            db.close()
            return
        
        # Create test user
        test_user = User(
            email="test@test.com",
            username="testuser",
            hashed_password=get_password_hash("password123"),
            role="patient",
            is_active=True,
            is_verified=True
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print(f"✅ Created test user: test@test.com / password123 (ID: {test_user.id})")
        
        # Create patient profile
        patient_profile = PatientProfile(
            user_id=test_user.id,
            first_name="Test",
            last_name="User"
        )
        db.add(patient_profile)
        db.commit()
        
        print("✅ Created patient profile")
        db.close()
        
    except Exception as e:
        print(f"❌ Failed to create test user: {e}")

if __name__ == "__main__":
    check_database()
    create_test_user()
    print("\n🎯 Test credentials:")
    print("   Email: test@test.com")
    print("   Password: password123")
