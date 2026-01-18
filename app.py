from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import cv2
import base64
import io
import os
from PIL import Image
import sqlite3
import numpy as np
import random
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
import urllib.request
import json
import warnings

# Suppress TensorFlow and other warnings
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logging

# Try to import deepface for emotion detection (suppress tensorflow errors)
DEEPFACE_AVAILABLE = False
try:
    import warnings
    warnings.filterwarnings('ignore')  # Suppress TensorFlow warnings
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except Exception as e:
    # Silently fail - we have a good fallback
    pass

# Create necessary directories
os.makedirs('ml_model', exist_ok=True)
os.makedirs('static/music', exist_ok=True)
os.makedirs('static/uploads', exist_ok=True)
os.makedirs('database', exist_ok=True)
os.makedirs('temp', exist_ok=True)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a random secret key
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac', 'm4a'}
CORS(app)

# Initialize emotion detection model
emotion_model = None
emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

def load_emotion_model():
    """Initialize emotion detection - uses deepface if available, otherwise feature-based fallback"""
    if DEEPFACE_AVAILABLE:
        print("Emotion detection ready (using DeepFace pre-trained model)")
    else:
        print("Emotion detection ready (using image feature analysis)")
    return True

def detect_emotion(image):
    """
    Detect emotion using deepface pre-trained model
    Falls back to feature analysis if deepface unavailable
    """
    try:
        # Try deepface first
        if DEEPFACE_AVAILABLE:
            try:
                # Save temporary image for deepface
                temp_path = 'temp/emotion_temp.jpg'
                cv2.imwrite(temp_path, image)
                
                # Analyze with deepface
                result = DeepFace.analyze(temp_path, actions=['emotion'], enforce_detection=False)
                
                if result and len(result) > 0:
                    emotions = result[0]['emotion']
                    # Get dominant emotion
                    emotion = max(emotions, key=emotions.get)
                    confidence = emotions[emotion] / 100.0  # Convert to 0-1 scale
                    
                    # Clean up
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                    
                    return emotion, min(confidence, 0.99)
            except Exception as e:
                print(f"DeepFace error: {e}")
        
        # Fallback: Face detection + feature analysis
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return 'neutral', 0.5
        
        # Get largest face
        face = max(faces, key=lambda f: f[2] * f[3])
        x, y, w, h = face
        roi_gray = gray[y:y+h, x:x+w]
        
        return detect_emotion_fallback(roi_gray)
        
    except Exception as e:
        print(f"Error in emotion detection: {e}")
        return 'neutral', 0.5

def detect_emotion_fallback(roi_gray):
    """
    Improved fallback emotion detection using image features
    - Brightness: Happy emotions tend to have brighter faces
    - Contrast: Anger/surprise have higher contrast  
    - Laplacian variance: Detailed features indicate certain emotions
    """
    try:
        # Resize for consistent analysis
        roi_gray = cv2.resize(roi_gray, (100, 100))
        brightness = np.mean(roi_gray)
        contrast = np.std(roi_gray)
        laplacian_var = cv2.Laplacian(roi_gray, cv2.CV_64F).var()
        # Normalize features
        brightness_norm = brightness / 255.0
        contrast_norm = min(contrast, 100.0) / 100.0
        laplacian_norm = min(laplacian_var, 2000.0) / 2000.0

        # Define ideal feature values for each emotion
        emotion_ideals = {
            'happy':    (0.85, 0.5, 0.2),   # bright, moderate contrast, low detail
            'sad':     (0.2, 0.2, 0.1),    # dark, low contrast, low detail
            'angry':   (0.5, 0.9, 0.7),    # mid-bright, high contrast, high detail
            'surprise':(0.9, 0.9, 0.5),    # very bright, very high contrast, med detail
            'fear':    (0.3, 0.5, 0.9),    # dark, med contrast, high detail
            'disgust': (0.5, 0.7, 0.8),    # mid-bright, med-high contrast, high detail
            'neutral': (0.5, 0.4, 0.3),    # mid everything
        }
        emotion_scores = {}
        for emotion, (ideal_b, ideal_c, ideal_l) in emotion_ideals.items():
            # Score is inverse of distance from ideal, weighted
            dist_b = abs(brightness_norm - ideal_b)
            dist_c = abs(contrast_norm - ideal_c)
            dist_l = abs(laplacian_norm - ideal_l)
            score = 0.4 * (1 - dist_b) + 0.3 * (1 - dist_c) + 0.3 * (1 - dist_l)
            # Sharpen neutral: only allow if all features are very close to ideal
            if emotion == 'neutral':
                if dist_b > 0.12 or dist_c > 0.12 or dist_l > 0.12:
                    score -= 0.3  # penalize neutral if any feature is not close
            emotion_scores[emotion] = score
        # If neutral is still highest, but another emotion is within 0.08, pick the non-neutral
        sorted_emotions = sorted(emotion_scores.items(), key=lambda x: -x[1])
        if sorted_emotions[0][0] == 'neutral' and len(sorted_emotions) > 1:
            if sorted_emotions[0][1] - sorted_emotions[1][1] < 0.08:
                emotion = sorted_emotions[1][0]
                confidence = max(0.5, min(0.95, sorted_emotions[1][1]))
                return emotion, confidence
        emotion = sorted_emotions[0][0]
        confidence = max(0.5, min(0.95, sorted_emotions[0][1]))
        return emotion, confidence
    except Exception as e:
        print(f"Fallback detection error: {e}")
        return 'neutral', 0.5

# Load emotion detection model at startup
print("Initializing emotion detection model...")
load_emotion_model()

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username, email, is_admin=False):
        self.id = id
        self.username = username
        self.email = email
        self.is_admin = is_admin

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, is_admin FROM users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        return User(user_data[0], user_data[1], user_data[2], bool(user_data[3]))
    return None

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return jsonify({'success': False, 'message': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, password_hash, is_admin FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data and check_password_hash(user_data[3], password):
            user = User(user_data[0], user_data[1], user_data[2], bool(user_data[4]))
            login_user(user)
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password'})
    
    return jsonify({'success': False, 'message': 'Invalid request method'})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'success': False, 'message': 'All fields are required'})
    
    password_hash = generate_password_hash(password)
    
    try:
        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash)
        )
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Registration successful'})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'message': 'Username or email already exists'})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'success': True, 'message': 'Logout successful'})

@app.route('/user_info')
@login_required
def user_info():
    return jsonify({
        'success': True,
        'user': {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'is_admin': current_user.is_admin
        }
    })

@app.route('/add_favorite', methods=['POST'])
@login_required
def add_favorite():
    data = request.get_json()
    song_id = data.get('song_id')
    
    try:
        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO favorites (user_id, song_id) VALUES (?, ?)",
            (current_user.id, song_id)
        )
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Song added to favorites'})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'message': 'Song already in favorites'})

@app.route('/remove_favorite', methods=['POST'])
@login_required
def remove_favorite():
    data = request.get_json()
    song_id = data.get('song_id')
    
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM favorites WHERE user_id = ? AND song_id = ?",
        (current_user.id, song_id)
    )
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Song removed from favorites'})

@app.route('/get_favorites')
@login_required
def get_favorites():
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.id, s.title, s.artist, s.file_path 
        FROM songs s
        JOIN favorites f ON s.id = f.song_id
        WHERE f.user_id = ?
    ''', (current_user.id,))
    
    favorites = cursor.fetchall()
    conn.close()
    
    favorite_songs = [{
        'id': song[0],
        'title': song[1],
        'artist': song[2],
        'file_path': song[3]
    } for song in favorites]
    
    return jsonify({'success': True, 'favorites': favorite_songs})

@app.route('/save_preferences', methods=['POST'])
@login_required
def save_preferences():
    data = request.get_json()
    preferred_genre = data.get('preferred_genre')
    preferred_artist = data.get('preferred_artist')
    
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    # Check if preferences already exist
    cursor.execute("SELECT id FROM user_preferences WHERE user_id = ?", (current_user.id,))
    existing_prefs = cursor.fetchone()
    
    if existing_prefs:
        # Update existing preferences
        cursor.execute(
            "UPDATE user_preferences SET preferred_genre = ?, preferred_artist = ?, updated_at = ? WHERE user_id = ?",
            (preferred_genre, preferred_artist, datetime.now(), current_user.id)
        )
    else:
        # Insert new preferences
        cursor.execute(
            "INSERT INTO user_preferences (user_id, preferred_genre, preferred_artist) VALUES (?, ?, ?)",
            (current_user.id, preferred_genre, preferred_artist)
        )
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Preferences saved successfully'})

@app.route('/get_preferences')
@login_required
def get_preferences():
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT preferred_genre, preferred_artist FROM user_preferences WHERE user_id = ?",
        (current_user.id,)
    )
    
    prefs = cursor.fetchone()
    conn.close()
    
    preferences = {
        'preferred_genre': prefs[0] if prefs else None,
        'preferred_artist': prefs[1] if prefs else None
    }
    
    return jsonify({'success': True, 'preferences': preferences})

@app.route('/analyze', methods=['POST'])
@login_required
def analyze_emotion():
    try:
        # Get image data from request
        data = request.get_json()
        image_data = data['image'].split(',')[1]  # Remove data:image/jpeg;base64, prefix
        image_bytes = base64.b64decode(image_data)
        
        # Convert to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to OpenCV format
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Detect emotion
        emotion, confidence = detect_emotion(image_cv)
        
        # Save to emotion history
        try:
            conn = sqlite3.connect('database/database.db')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO emotion_history (user_id, emotion, confidence) VALUES (?, ?, ?)",
                (current_user.id, emotion, confidence)
            )
            conn.commit()
            conn.close()
        except Exception as hist_error:
            print(f"Error saving emotion history: {hist_error}")
        
        return jsonify({
            'emotion': emotion,
            'confidence': confidence,
            'success': True
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        })

@app.route('/recommend', methods=['POST'])
@login_required
def recommend_music():
    try:
        data = request.get_json()
        emotion = data['emotion'].lower()
        
        # Use hybrid recommendation system for better results
        try:
            from ml_model.hybrid_recommender import get_personalized_recommendations
            recommendations = get_personalized_recommendations(current_user.id, emotion, n_recommendations=10)
        except Exception as hybrid_error:
            print(f"Hybrid recommender error: {hybrid_error}")
            # Fallback to basic KNN
            from ml_model.recommendation_engine import get_recommendations
            recommendations = get_recommendations(emotion)
        
        return jsonify({
            'songs': recommendations,
            'success': True,
            'algorithm': 'hybrid'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        })


# Track song play
@app.route('/track_play', methods=['POST'])
@login_required
def track_play():
    """Track when a user plays a song"""
    try:
        data = request.get_json()
        song_id = data.get('song_id')
        
        if not song_id:
            return jsonify({'success': False, 'message': 'Song ID required'})
        
        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()
        
        # Add to listening history
        cursor.execute(
            "INSERT INTO listening_history (user_id, song_id) VALUES (?, ?)",
            (current_user.id, song_id)
        )
        
        # Update play count in songs table
        cursor.execute(
            "UPDATE songs SET play_count = play_count + 1 WHERE id = ?",
            (song_id,)
        )
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Play tracked'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# Get emotion history
@app.route('/emotion_history')
@login_required
def get_emotion_history():
    """Get user's emotion history"""
    try:
        limit = request.args.get('limit', 50, type=int)
        
        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT emotion, confidence, timestamp
            FROM emotion_history
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (current_user.id, limit))
        
        history = cursor.fetchall()
        conn.close()
        
        emotion_list = [{
            'emotion': row[0],
            'confidence': row[1],
            'timestamp': row[2]
        } for row in history]
        
        return jsonify({
            'success': True,
            'history': emotion_list
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# Get emotion statistics
@app.route('/emotion_stats')
@login_required
def get_emotion_stats():
    """Get user's emotion statistics"""
    try:
        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()
        
        # Get emotion distribution
        cursor.execute('''
            SELECT emotion, COUNT(*) as count
            FROM emotion_history
            WHERE user_id = ?
            GROUP BY emotion
            ORDER BY count DESC
        ''', (current_user.id,))
        
        distribution = cursor.fetchall()
        
        # Get total emotions captured
        cursor.execute('''
            SELECT COUNT(*) FROM emotion_history WHERE user_id = ?
        ''', (current_user.id,))
        
        total = cursor.fetchone()[0]
        
        conn.close()
        
        stats = {
            'total_captures': total,
            'distribution': [{'emotion': row[0], 'count': row[1]} for row in distribution]
        }
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# Get listening history
@app.route('/listening_history')
@login_required
def get_listening_history():
    """Get user's listening history"""
    try:
        limit = request.args.get('limit', 50, type=int)
        
        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT s.id, s.title, s.artist, s.file_path, s.emotion_tag, lh.timestamp
            FROM listening_history lh
            JOIN songs s ON lh.song_id = s.id
            WHERE lh.user_id = ?
            ORDER BY lh.timestamp DESC
            LIMIT ?
        ''', (current_user.id, limit))
        
        history = cursor.fetchall()
        conn.close()
        
        listening_list = [{
            'id': row[0],
            'title': row[1],
            'artist': row[2],
            'file_path': row[3],
            'emotion_tag': row[4],
            'timestamp': row[5]
        } for row in history]
        
        return jsonify({
            'success': True,
            'history': listening_list
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# Get most played songs
@app.route('/most_played')
@login_required
def get_most_played():
    """Get user's most played songs"""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT s.id, s.title, s.artist, s.file_path, COUNT(*) as play_count
            FROM listening_history lh
            JOIN songs s ON lh.song_id = s.id
            WHERE lh.user_id = ?
            GROUP BY s.id
            ORDER BY play_count DESC
            LIMIT ?
        ''', (current_user.id, limit))
        
        most_played = cursor.fetchall()
        conn.close()
        
        songs_list = [{
            'id': row[0],
            'title': row[1],
            'artist': row[2],
            'file_path': row[3],
            'play_count': row[4]
        } for row in most_played]
        
        return jsonify({
            'success': True,
            'songs': songs_list
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/upload_song', methods=['POST'])
@login_required
def upload_song():
    try:
        if 'audio_file' not in request.files:
            return jsonify({'success': False, 'message': 'No file uploaded'})
        
        file = request.files['audio_file']
        title = request.form.get('title')
        artist = request.form.get('artist')
        emotion_tag = request.form.get('emotion_tag')
        valence = float(request.form.get('valence', 0.5))
        energy = float(request.form.get('energy', 0.5))
        
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'})
        
        if not title or not artist or not emotion_tag:
            return jsonify({'success': False, 'message': 'All fields are required'})
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add timestamp to avoid conflicts
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Save to database
            conn = sqlite3.connect('database/database.db')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO songs (title, artist, file_path, emotion_tag, valence, energy, uploaded_by) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (title, artist, f'/static/uploads/{filename}', emotion_tag.lower(), valence, energy, current_user.id)
            )
            conn.commit()
            conn.close()
            
            return jsonify({'success': True, 'message': 'Song uploaded successfully'})
        else:
            return jsonify({'success': False, 'message': 'Invalid file type. Allowed: mp3, wav, ogg, flac, m4a'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# Admin routes
@app.route('/admin/panel')
@login_required
@admin_required
def admin_panel():
    return render_template('admin.html')

@app.route('/admin/users')
@login_required
@admin_required
def get_users():
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, is_admin, created_at FROM users")
    users_data = cursor.fetchall()
    conn.close()
    
    users = [{
        'id': user[0],
        'username': user[1],
        'email': user[2],
        'is_admin': bool(user[3]),
        'created_at': user[4]
    } for user in users_data]
    
    return jsonify({'success': True, 'users': users})

@app.route('/admin/songs')
@login_required
@admin_required
def get_all_songs():
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.id, s.title, s.artist, s.file_path, s.emotion_tag, s.valence, s.energy, 
               u.username, s.created_at
        FROM songs s
        LEFT JOIN users u ON s.uploaded_by = u.id
    ''')
    songs_data = cursor.fetchall()
    conn.close()
    
    songs = [{
        'id': song[0],
        'title': song[1],
        'artist': song[2],
        'file_path': song[3],
        'emotion_tag': song[4],
        'valence': song[5],
        'energy': song[6],
        'uploaded_by': song[7] if song[7] else 'System',
        'created_at': song[8]
    } for song in songs_data]
    
    return jsonify({'success': True, 'songs': songs})

@app.route('/admin/delete_song/<int:song_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_song(song_id):
    try:
        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()
        
        # Get file path before deleting
        cursor.execute("SELECT file_path FROM songs WHERE id = ?", (song_id,))
        result = cursor.fetchone()
        
        if result:
            file_path = result[0]
            # Delete file from disk if it exists
            if file_path.startswith('/static/uploads/'):
                full_path = file_path.replace('/static/', 'static/')
                if os.path.exists(full_path):
                    os.remove(full_path)
            
            # Delete from database
            cursor.execute("DELETE FROM songs WHERE id = ?", (song_id,))
            cursor.execute("DELETE FROM favorites WHERE song_id = ?", (song_id,))
            conn.commit()
            conn.close()
            
            return jsonify({'success': True, 'message': 'Song deleted successfully'})
        else:
            conn.close()
            return jsonify({'success': False, 'message': 'Song not found'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/update_user/<int:user_id>', methods=['PUT'])
@login_required
@admin_required
def update_user(user_id):
    try:
        data = request.get_json()
        is_admin = data.get('is_admin', False)
        
        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET is_admin = ? WHERE id = ?", (int(is_admin), user_id))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'User updated successfully'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/delete_user/<int:user_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_user(user_id):
    try:
        if user_id == current_user.id:
            return jsonify({'success': False, 'message': 'Cannot delete your own account'})
        
        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        cursor.execute("DELETE FROM favorites WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM user_preferences WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'User deleted successfully'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/stats')
@login_required
@admin_required
def get_stats():
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM songs")
    total_songs = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM favorites")
    total_favorites = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT emotion_tag, COUNT(*) as count 
        FROM songs 
        GROUP BY emotion_tag 
        ORDER BY count DESC
    """)
    song_emotion_distribution = cursor.fetchall()
    
    # New: Total emotion captures
    cursor.execute("SELECT COUNT(*) FROM emotion_history")
    total_emotion_captures = cursor.fetchone()[0]
    
    # New: Emotion capture distribution
    cursor.execute("""
        SELECT emotion, COUNT(*) as count
        FROM emotion_history
        GROUP BY emotion
        ORDER BY count DESC
    """)
    emotion_captures_distribution = cursor.fetchall()
    
    # New: Total song plays
    cursor.execute("SELECT COUNT(*) FROM listening_history")
    total_plays = cursor.fetchone()[0]
    
    # New: Most played songs
    cursor.execute("""
        SELECT s.title, s.artist, COUNT(*) as plays
        FROM listening_history lh
        JOIN songs s ON lh.song_id = s.id
        GROUP BY s.id
        ORDER BY plays DESC
        LIMIT 10
    """)
    most_played_songs = cursor.fetchall()
    
    # New: Active users (users with recent activity)
    cursor.execute("""
        SELECT COUNT(DISTINCT user_id)
        FROM emotion_history
        WHERE timestamp >= datetime('now', '-7 days')
    """)
    active_users_week = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'success': True,
        'stats': {
            'total_users': total_users,
            'total_songs': total_songs,
            'total_favorites': total_favorites,
            'total_emotion_captures': total_emotion_captures,
            'total_plays': total_plays,
            'active_users_week': active_users_week,
            'song_emotion_distribution': [{'emotion': e[0], 'count': e[1]} for e in song_emotion_distribution],
            'emotion_captures_distribution': [{'emotion': e[0], 'count': e[1]} for e in emotion_captures_distribution],
            'most_played_songs': [{'title': s[0], 'artist': s[1], 'plays': s[2]} for s in most_played_songs]
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)