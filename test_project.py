"""
Test script for Emotion Music Recommender System
Tests all major functionality
"""
import requests
import json
import os

BASE_URL = "http://localhost:5000"

def print_result(test_name, success, message=""):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} - {test_name}")
    if message:
        print(f"   → {message}")
    print()

def test_home_page():
    """Test if home page loads"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print_result("Home Page Load", response.status_code == 200)
        return response.status_code == 200
    except Exception as e:
        print_result("Home Page Load", False, str(e))
        return False

def test_register():
    """Test user registration"""
    try:
        data = {
            "username": "testuser123",
            "email": "test@example.com",
            "password": "testpass123"
        }
        response = requests.post(f"{BASE_URL}/register", json=data)
        result = response.json()
        
        # Registration might fail if user exists, which is ok
        success = result.get('success', False)
        message = result.get('message', '')
        
        if "already exists" in message:
            print_result("User Registration", True, "User already exists (OK)")
            return True
        else:
            print_result("User Registration", success, message)
            return success
    except Exception as e:
        print_result("User Registration", False, str(e))
        return False

def test_login():
    """Test user login"""
    try:
        # Try with test user first
        data = {
            "username": "testuser123",
            "password": "testpass123"
        }
        response = requests.post(f"{BASE_URL}/login", json=data)
        result = response.json()
        
        if not result.get('success'):
            # Try with admin credentials
            data = {
                "username": "admin",
                "password": "admin123"
            }
            response = requests.post(f"{BASE_URL}/login", json=data)
            result = response.json()
        
        success = result.get('success', False)
        message = result.get('message', '')
        print_result("User Login", success, message)
        
        # Return session for further tests
        return response.cookies if success else None
    except Exception as e:
        print_result("User Login", False, str(e))
        return None

def test_admin_login():
    """Test admin login"""
    try:
        data = {
            "username": "admin",
            "password": "admin123"
        }
        response = requests.post(f"{BASE_URL}/login", json=data)
        result = response.json()
        success = result.get('success', False)
        message = result.get('message', '')
        print_result("Admin Login", success, message)
        return response.cookies if success else None
    except Exception as e:
        print_result("Admin Login", False, str(e))
        return None

def test_user_info(cookies):
    """Test getting user info"""
    if not cookies:
        print_result("Get User Info", False, "No session cookies")
        return False
    
    try:
        response = requests.get(f"{BASE_URL}/user_info", cookies=cookies)
        result = response.json()
        success = result.get('success', False)
        
        if success:
            user = result.get('user', {})
            message = f"User: {user.get('username')}, Admin: {user.get('is_admin')}"
        else:
            message = result.get('message', 'Failed')
        
        print_result("Get User Info", success, message)
        return success
    except Exception as e:
        print_result("Get User Info", False, str(e))
        return False

def test_admin_stats(cookies):
    """Test admin statistics"""
    if not cookies:
        print_result("Admin Stats", False, "No session cookies")
        return False
    
    try:
        response = requests.get(f"{BASE_URL}/admin/stats", cookies=cookies)
        result = response.json()
        success = result.get('success', False)
        
        if success:
            stats = result.get('stats', {})
            message = f"Users: {stats.get('total_users')}, Songs: {stats.get('total_songs')}, Favorites: {stats.get('total_favorites')}"
        else:
            message = result.get('message', 'Failed')
        
        print_result("Admin Statistics", success, message)
        return success
    except Exception as e:
        print_result("Admin Statistics", False, str(e))
        return False

def test_get_recommendations():
    """Test music recommendations"""
    try:
        data = {"emotion": "happy"}
        response = requests.post(f"{BASE_URL}/recommend", json=data)
        result = response.json()
        success = result.get('success', False)
        
        if success:
            songs = result.get('songs', [])
            message = f"Got {len(songs)} recommendations"
        else:
            message = result.get('error', 'Failed')
        
        print_result("Music Recommendations", success, message)
        return success
    except Exception as e:
        print_result("Music Recommendations", False, str(e))
        return False

def test_database():
    """Test database connectivity"""
    try:
        import sqlite3
        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()
        
        # Check tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['users', 'songs', 'favorites', 'user_preferences']
        all_exist = all(table in tables for table in required_tables)
        
        if all_exist:
            # Count records
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM songs")
            song_count = cursor.fetchone()[0]
            
            message = f"Users: {user_count}, Songs: {song_count}"
        else:
            message = f"Missing tables: {set(required_tables) - set(tables)}"
        
        conn.close()
        print_result("Database Connection", all_exist, message)
        return all_exist
    except Exception as e:
        print_result("Database Connection", False, str(e))
        return False

def test_file_structure():
    """Test if required files and folders exist"""
    required_paths = [
        'static/css/style.css',
        'static/js/script.js',
        'static/uploads',
        'static/music',
        'templates/index.html',
        'templates/admin.html',
        'database/database.db',
        'ml_model/recommendation_engine.py'
    ]
    
    all_exist = True
    missing = []
    
    for path in required_paths:
        if not os.path.exists(path):
            all_exist = False
            missing.append(path)
    
    if all_exist:
        message = "All required files exist"
    else:
        message = f"Missing: {', '.join(missing)}"
    
    print_result("File Structure", all_exist, message)
    return all_exist

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🧪 TESTING EMOTION MUSIC RECOMMENDER SYSTEM")
    print("=" * 60)
    print()
    
    # Test 1: File Structure
    print("📁 Testing File Structure...")
    test_file_structure()
    
    # Test 2: Database
    print("🗄️ Testing Database...")
    test_database()
    
    # Test 3: Server
    print("🌐 Testing Server Endpoints...")
    test_home_page()
    
    # Test 4: Authentication
    print("🔐 Testing Authentication...")
    test_register()
    cookies = test_login()
    admin_cookies = test_admin_login()
    
    # Test 5: User Features
    print("👤 Testing User Features...")
    test_user_info(admin_cookies if admin_cookies else cookies)
    
    # Test 6: Recommendations
    print("🎵 Testing Music Recommendations...")
    test_get_recommendations()
    
    # Test 7: Admin Features
    print("⚙️ Testing Admin Features...")
    test_admin_stats(admin_cookies)
    
    print()
    print("=" * 60)
    print("✅ TESTING COMPLETE!")
    print("=" * 60)
    print()
    print("🌐 Application running at: http://localhost:5000")
    print("🔑 Admin Login: admin / admin123")
    print()

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⚠️ Testing interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Testing failed with error: {e}")
