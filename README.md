# 🎵 Emotion-Based Music Recommender System

A sophisticated web-based application that detects user emotions through facial recognition and recommends music accordingly. Built with Flask, OpenCV, and machine learning - **No external APIs required!**

![Python](https://img.shields.io/badge/python-3.8+-green)

## ✨ Features

### 🎭 Core Functionality

- **Real-time Emotion Detection**: Uses webcam to detect facial emotions with confidence scores
- **Smart Music Recommendations**: AI-powered song suggestions based on detected emotions using KNN algorithm
- **Built-in Audio Player**: Play recommended songs directly in your browser with full controls
- **Song Upload System**: Users can upload their own music with emotion tags and metadata
- **Favorites Management**: Save and organize your favorite songs for quick access
- **User Profiles**: Personalized preferences for genres and artists

### 🔐 Admin Features

- **Comprehensive Admin Panel**: Full-featured dashboard for system management
- **User Management**: Create, update, delete users and manage admin roles
- **Song Management**: Complete CRUD operations for the entire music library
- **Analytics Dashboard**: Real-time statistics including:
  - Total users count
  - Total songs in library
  - Favorite tracks statistics
  - Emotion distribution charts
- **System Controls**: Complete administrative privileges

### 👤 User Features

- **Upload Your Music**: Add songs from your device with metadata (title, artist, emotion tags)
- **Emotion-Based Filtering**: Get songs matching your current mood automatically
- **Favorites System**: Save songs you love and access them anytime
- **User Preferences**: Set your favorite genres and artists for personalized recommendations
- **Secure Authentication**: Login/register system with password hashing

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Webcam (for emotion detection)
- Modern web browser (Chrome, Firefox, Edge, Safari)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/Ikshang/Emotion-based-music-recommender.git
cd Emotion-based-music-recommender
```

2. **Create and activate virtual environment**

Windows:

```bash
python -m venv emotion_env
emotion_env\Scripts\activate
```

Linux/Mac:

```bash
python3 -m venv emotion_env
source emotion_env/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Initialize the database**

```bash
python database/init_database.py
```

5. **Run the application**

```bash
python app.py
```

6. **Open your browser**

```
http://localhost:5000
```

## 🔑 Default Credentials

### Admin Account

- **Username**: `admin`
- **Password**: `admin123`
- **Access**: Full system privileges including admin panel

⚠️ **Security Notice**: Change the default admin password immediately after first login!

## 📖 User Guide

### For Regular Users

#### 1. Getting Started

1. Register a new account or login
2. Allow camera access when prompted
3. Set your music preferences (optional)

#### 2. Emotion Detection

1. Click **"Start Camera"** to enable your webcam
2. Position your face in the camera frame
3. Click **"Capture Emotion"** to analyze your expression
4. View your detected emotion and confidence score

#### 3. Music Recommendations

- Songs are automatically recommended based on your detected emotion
- Browse the list of suggested songs
- Click **"Play"** to listen to any song
- Click **♥** to add songs to your favorites

#### 4. Upload Your Own Music

1. Click **"Upload Song"** button in the navigation bar
2. Fill in the song details:
   - **Title**: Song name
   - **Artist**: Artist or band name
   - **Emotion Tag**: Select the emotion this song represents
   - **Valence**: Positivity level (0-1, where 1 is most positive)
   - **Energy**: Energy level (0-1, where 1 is most energetic)
3. Choose your audio file (MP3, WAV, OGG, FLAC, or M4A)
4. Click **"Upload Song"**

#### 5. Manage Favorites

- Click **"Favorites"** to view all your saved songs
- Play songs directly from your favorites
- Remove songs from favorites if desired

### For Administrators

#### 1. Access Admin Panel

1. Login with admin credentials
2. Click **"Admin Panel"** button (visible only to admins)

#### 2. Dashboard Overview

The admin dashboard displays:

- **Total Users**: Count of registered users
- **Total Songs**: Number of songs in library
- **Total Favorites**: Number of favorite entries
- **Emotion Distribution**: Breakdown of songs by emotion tag

#### 3. User Management

- View all registered users with their details
- **Make Admin**: Grant admin privileges to users
- **Remove Admin**: Revoke admin privileges
- **Delete User**: Remove user accounts (cannot delete yourself)

#### 4. Song Management

- View complete music library with metadata
- See who uploaded each song
- Delete songs from the system
- Songs uploaded by deleted users remain in the system

#### 5. Upload Songs as Admin

- Same upload process as regular users
- Can manage all uploaded songs regardless of uploader

## 🎨 Emotion System

### Supported Emotions

| Emotion         | Description         | Music Characteristics          |
| --------------- | ------------------- | ------------------------------ |
| 😊 **Happy**    | Joyful, cheerful    | Upbeat, positive, high valence |
| 😢 **Sad**      | Melancholic, down   | Slower tempo, low valence      |
| 😠 **Angry**    | Frustrated, intense | High energy, aggressive        |
| 😐 **Neutral**  | Calm, balanced      | Ambient, moderate tempo        |
| 😲 **Surprise** | Excited, unexpected | Dynamic, high energy           |
| 😨 **Fear**     | Anxious, tense      | Atmospheric, suspenseful       |

### Valence & Energy Explained

- **Valence (0-1)**: Measures musical positivity

  - 0.0-0.3: Sad, dark, negative
  - 0.4-0.6: Neutral, balanced
  - 0.7-1.0: Happy, bright, positive

- **Energy (0-1)**: Measures intensity and activity
  - 0.0-0.3: Calm, peaceful, slow
  - 0.4-0.6: Moderate tempo
  - 0.7-1.0: Energetic, intense, fast

## 🛠️ Technology Stack

### Backend Technologies

- **Flask 2.2.2**: Web framework
- **Flask-Login 0.6.2**: User session management
- **Flask-CORS 3.0.10**: Cross-origin resource sharing
- **SQLite**: Embedded database
- **Werkzeug 2.2.3**: Security utilities (password hashing)

### Machine Learning & Computer Vision

- **OpenCV 4.6.0**: Facial detection and image processing
- **NumPy 1.23.3**: Numerical computing
- **Pandas 1.5.0**: Data manipulation
- **Scikit-learn 1.1.2**: Machine learning algorithms (KNN for recommendations)

### Frontend Technologies

- **Bootstrap 5.1.3**: Responsive UI framework
- **Vanilla JavaScript**: Frontend logic and interactions
- **HTML5 Audio API**: Music playback
- **MediaDevices API**: Webcam access
- **Canvas API**: Image processing

## 📁 Project Structure

```
Emotion Music Recommend System/
│
├── app.py                          # Main Flask application with all routes
├── requirements.txt                # Python package dependencies
├── README.md                       # This file
├── PROJECT_IMPROVEMENTS.md         # Future enhancement suggestions
│
├── database/
│   ├── init_database.py           # Database schema and initialization
│   ├── data_wrangler.py           # Data processing utilities
│   └── database.db                # SQLite database (auto-created)
│
├── ml_model/
│   ├── recommendation_engine.py   # KNN-based recommendation algorithm
│   └── models/                    # Placeholder for ML model files
│
├── static/
│   ├── css/
│   │   └── style.css             # Custom styles and animations
│   ├── js/
│   │   └── script.js             # Frontend JavaScript logic
│   ├── music/                     # Default/system music storage
│   └── uploads/                   # User-uploaded songs (auto-created)
│
├── templates/
│   ├── index.html                 # Main application page
│   └── admin.html                 # Admin panel interface
│
└── temp/                          # Temporary files (auto-created)
```

## 📊 Database Schema

### Tables Overview

#### users

| Column        | Type      | Description           |
| ------------- | --------- | --------------------- |
| id            | INTEGER   | Primary key           |
| username      | TEXT      | Unique username       |
| email         | TEXT      | Unique email address  |
| password_hash | TEXT      | Hashed password       |
| is_admin      | INTEGER   | Admin flag (0 or 1)   |
| created_at    | TIMESTAMP | Account creation date |

#### songs

| Column      | Type      | Description         |
| ----------- | --------- | ------------------- |
| id          | INTEGER   | Primary key         |
| title       | TEXT      | Song title          |
| artist      | TEXT      | Artist name         |
| file_path   | TEXT      | Path to audio file  |
| emotion_tag | TEXT      | Associated emotion  |
| valence     | REAL      | Positivity (0-1)    |
| energy      | REAL      | Energy level (0-1)  |
| uploaded_by | INTEGER   | User ID of uploader |
| created_at  | TIMESTAMP | Upload date         |

#### favorites

| Column     | Type      | Description             |
| ---------- | --------- | ----------------------- |
| id         | INTEGER   | Primary key             |
| user_id    | INTEGER   | Foreign key to users    |
| song_id    | INTEGER   | Foreign key to songs    |
| created_at | TIMESTAMP | Date added to favorites |

#### user_preferences

| Column           | Type      | Description          |
| ---------------- | --------- | -------------------- |
| id               | INTEGER   | Primary key          |
| user_id          | INTEGER   | Foreign key to users |
| preferred_genre  | TEXT      | Favorite genre       |
| preferred_artist | TEXT      | Favorite artist      |
| created_at       | TIMESTAMP | Creation date        |
| updated_at       | TIMESTAMP | Last update date     |

## 🔒 Security Features

- ✅ **Password Hashing**: Werkzeug's secure password hashing
- ✅ **File Validation**: Strict file type checking for uploads
- ✅ **Size Limits**: 50MB maximum file size
- ✅ **Secure Filenames**: Sanitization of uploaded filenames
- ✅ **Admin Protection**: Decorator-based route protection
- ✅ **Session Management**: Flask-Login secure sessions
- ✅ **SQL Injection Prevention**: Parameterized queries
- ✅ **CORS Configuration**: Controlled cross-origin requests

## 🎵 Supported Audio Formats

| Format | Extension | Quality   | Size   |
| ------ | --------- | --------- | ------ |
| MP3    | .mp3      | Good      | Small  |
| WAV    | .wav      | Excellent | Large  |
| OGG    | .ogg      | Good      | Medium |
| FLAC   | .flac     | Excellent | Large  |
| M4A    | .m4a      | Good      | Small  |

**Max File Size**: 50MB per upload

## ⚙️ Configuration

### Change Secret Key (Important!)

Edit `app.py`:

```python
app.secret_key = 'your-very-secure-random-secret-key-here'
```

Generate a secure key:

```python
import secrets
print(secrets.token_hex(32))
```

### Adjust Upload Settings

Edit `app.py`:

```python
# Maximum file size (in bytes)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

# Upload folder location
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Allowed file extensions
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac', 'm4a'}
```

### Database Location

Edit connection strings in `app.py` and `init_database.py`:

```python
conn = sqlite3.connect('database/database.db')
```

## 🐛 Troubleshooting

### Camera Issues

**Problem**: Camera not working or permission denied

**Solutions**:

- Check browser permissions (allow camera access)
- Ensure camera is not being used by another application
- Try a different browser (Chrome recommended)
- Check if HTTPS is required by your browser
- Restart the browser

### Audio Playback Issues

**Problem**: Songs not playing

**Solutions**:

- Verify audio file format is supported
- Check browser console for errors
- Ensure file path is correct
- Test with different audio formats
- Check volume settings

### Upload Failures

**Problem**: Cannot upload songs

**Solutions**:

- Check file size (max 50MB)
- Verify file format is in allowed list
- Ensure sufficient disk space
- Check folder permissions on `static/uploads/`
- Try smaller file or different format

### Database Errors

**Problem**: Database connection or query errors

**Solutions**:

- Run `python database/init_database.py` to recreate database
- Check file permissions on `database/` folder
- Ensure SQLite3 is installed
- Delete `database.db` and reinitialize

### Login Issues

**Problem**: Cannot login or register

**Solutions**:

- Check if database is initialized
- Verify username/password are correct
- Clear browser cookies and cache
- Check console for error messages

## 🚀 Future Enhancements

See `PROJECT_IMPROVEMENTS.md` for comprehensive list including:

### High Priority

1. **Advanced Emotion Detection**: Implement CNN-based model (FER-2013 dataset)
2. **Audio Visualization**: Waveform display and equalizer
3. **Playlist Management**: Create and share custom playlists
4. **Search Functionality**: Search songs by title, artist, or emotion

### Medium Priority

5. **User Dashboard**: Statistics and listening history
6. **Collaborative Filtering**: Better recommendations based on user behavior
7. **Audio Processing**: Auto-normalize, format conversion
8. **Performance Optimization**: Caching, lazy loading

### Nice to Have

9. **Dark Theme**: Toggle between light and dark modes
10. **Social Features**: Follow users, share playlists
11. **Achievement System**: Badges and milestones
12. **Mobile App**: React Native or Flutter version

## 📈 Performance Tips

- **Optimize Images**: Compress images before using
- **Use Pagination**: For large song lists
- **Enable Caching**: Implement Flask-Caching
- **Database Indexing**: Add indexes to frequently queried columns
- **Audio Streaming**: Stream large files instead of loading entirely
- **Lazy Loading**: Load content as needed

## 🧪 Testing

### Manual Testing Checklist

- [ ] User registration and login
- [ ] Camera access and emotion detection
- [ ] Song recommendations appear
- [ ] Audio playback works
- [ ] File upload functions
- [ ] Favorites add/remove
- [ ] Admin panel accessible
- [ ] User management (admin)
- [ ] Song management (admin)

### Future Automated Testing

- Unit tests with pytest
- Integration tests
- Selenium for UI testing
- Load testing with Locust

## 📝 API Endpoints

### Authentication

- `POST /login` - User login
- `POST /register` - User registration
- `GET /logout` - User logout
- `GET /user_info` - Get current user info

### Music & Recommendations

- `POST /analyze` - Analyze emotion from image
- `POST /recommend` - Get music recommendations
- `POST /upload_song` - Upload new song

### Favorites & Preferences

- `POST /add_favorite` - Add song to favorites
- `POST /remove_favorite` - Remove from favorites
- `GET /get_favorites` - Get user's favorites
- `POST /save_preferences` - Save user preferences
- `GET /get_preferences` - Get user preferences

### Admin Routes

- `GET /admin/panel` - Admin panel page
- `GET /admin/users` - Get all users
- `GET /admin/songs` - Get all songs
- `GET /admin/stats` - Get system statistics
- `PUT /admin/update_user/<id>` - Update user
- `DELETE /admin/delete_user/<id>` - Delete user
- `DELETE /admin/delete_song/<id>` - Delete song

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Guidelines

- Follow PEP 8 style guide for Python
- Add comments for complex logic
- Update documentation for new features
- Test thoroughly before submitting

## 👨‍💻 Author

**Manish**

- GitHub: [@Ikshang](https://github.com/Manishchm)

## 🙏 Acknowledgments

- OpenCV team for computer vision tools
- Flask community for excellent documentation
- Bootstrap team for responsive UI components
- Scikit-learn for machine learning algorithms

## ⭐ Show Your Support

If you found this project helpful, please consider:

- Giving it a ⭐ on GitHub
- Sharing it with others
- Contributing to its development
- Reporting bugs and suggesting features

## 📧 Support & Contact

- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions
- **Email**: Check GitHub profile for contact info

---

**Made with ❤️ for music lovers and emotion recognition enthusiasts**

_Last Updated: December 2025_
