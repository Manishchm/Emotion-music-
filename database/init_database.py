import sqlite3
import os
from werkzeug.security import generate_password_hash

def init_db():
    """Initialize database with all necessary tables"""
    # Create database directory
    os.makedirs('database', exist_ok=True)
    
    # Connect to SQLite database (will create if not exists)
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create songs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        artist TEXT NOT NULL,
        file_path TEXT NOT NULL,
        emotion_tag TEXT NOT NULL,
        valence REAL NOT NULL,
        energy REAL NOT NULL,
        uploaded_by INTEGER,
        play_count INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (uploaded_by) REFERENCES users (id)
    )
    ''')
    
    # Create favorites table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        song_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (song_id) REFERENCES songs (id),
        UNIQUE(user_id, song_id)
    )
    ''')
    
    # Create user preferences table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_preferences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        preferred_genre TEXT,
        preferred_artist TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Create emotion_history table - NEW!
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS emotion_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        emotion TEXT NOT NULL,
        confidence REAL NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Create listening_history table - NEW!
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS listening_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        song_id INTEGER NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (song_id) REFERENCES songs (id)
    )
    ''')
    
    # Create indexes for performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_emotion_history_user ON emotion_history(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_emotion_history_timestamp ON emotion_history(timestamp)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_listening_history_user ON listening_history(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_listening_history_song ON listening_history(song_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_listening_history_timestamp ON listening_history(timestamp)')
    
    # Create a default admin user
    try:
        admin_password = generate_password_hash("admin123")
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, is_admin) VALUES (?, ?, ?, ?)",
            ("admin", "admin@example.com", admin_password, 1)
        )
        print("✅ Admin user created (admin/admin123)")
    except sqlite3.IntegrityError:
        print("ℹ️  Admin user already exists")
    
    # Commit and close
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully with all tables!")
    print("   - users")
    print("   - songs")
    print("   - favorites")
    print("   - user_preferences")
    print("   - emotion_history (NEW)")
    print("   - listening_history (NEW)")

if __name__ == '__main__':
    init_db()