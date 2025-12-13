# Changelog

All notable changes to the Emotion Music Recommender System.

## [2.0.0] - 2025-12-12

### 🎉 Major New Features

#### User Song Upload System

- **Upload Your Own Music**: Users can now upload songs from their devices
- **Metadata Support**: Add title, artist, emotion tags, valence, and energy levels
- **Multi-format Support**: MP3, WAV, OGG, FLAC, M4A files accepted
- **File Validation**: Secure file type checking and size limits (50MB max)
- **User Attribution**: Track who uploaded each song

#### Admin Panel

- **Comprehensive Dashboard**: Beautiful admin interface with statistics
- **User Management**:
  - View all registered users
  - Promote/demote admin privileges
  - Delete user accounts
  - User creation date tracking
- **Song Management**:
  - View entire music library
  - See uploader information
  - Delete songs from system
  - Track upload dates
- **System Statistics**:
  - Total users count
  - Total songs in library
  - Favorites statistics
  - Emotion distribution charts
- **Admin Privileges**: Full CRUD operations on all resources

#### Enhanced Audio Playback

- **Fully Functional Player**: Songs are now completely playable in the browser
- **Play Controls**: Standard HTML5 audio controls
- **Now Playing Display**: Shows currently playing song with artist
- **Visual Feedback**: Active song highlighting
- **Queue System**: Play songs from recommendations or favorites

### 🔧 Technical Improvements

#### Database Schema Updates

- Added `is_admin` field to users table for role management
- Added `uploaded_by` field to songs table to track uploader
- Added `created_at` timestamps to all tables
- Foreign key relationships properly established

#### Security Enhancements

- **Admin Decorator**: Route protection for admin-only endpoints
- **File Upload Security**:
  - Secure filename sanitization
  - File type validation using extensions
  - Size limit enforcement
  - Safe file storage
- **Admin Role Management**: Proper permission system implemented

#### Backend Additions

- New routes for song upload (`/upload_song`)
- Admin panel routes:
  - `/admin/panel` - Admin dashboard
  - `/admin/users` - User management
  - `/admin/songs` - Song management
  - `/admin/stats` - System statistics
  - `/admin/update_user/<id>` - Update user role
  - `/admin/delete_user/<id>` - Delete user
  - `/admin/delete_song/<id>` - Delete song
- Enhanced user info endpoint with `is_admin` field
- File serving configuration for uploaded audio

#### Frontend Enhancements

- **Upload Modal**: Beautiful modal dialog for song uploads
- **Admin Panel UI**: Professional dashboard with:
  - Statistics cards with gradients
  - Tabbed interface for different sections
  - Responsive tables
  - Action buttons for management
- **Admin Panel Button**: Conditionally shown for admin users
- **Enhanced User Section**: Upload button in navigation
- **Improved Audio Player**: Better integration with recommendations

#### File Structure

- New `static/uploads/` directory for user-uploaded songs
- New `templates/admin.html` for admin panel
- Enhanced `app.py` with admin functionality
- Updated database initialization script

### 🐛 Bug Fixes

- Fixed audio player not playing recommended songs
- Improved error handling for file uploads
- Better session management for admin users
- Fixed file path handling for uploaded songs

### 📚 Documentation

- **README_NEW.md**: Comprehensive documentation covering:
  - Complete feature list
  - Installation instructions
  - User guide for regular users
  - Admin guide
  - Troubleshooting section
  - API documentation
  - Security information
- **PROJECT_IMPROVEMENTS.md**: Detailed enhancement suggestions
- **Setup Scripts**: Automated setup for Windows (setup.bat) and Linux/Mac (setup.sh)
- **Run Script**: Quick start script (run.bat)
- **CHANGELOG.md**: This file documenting all changes

### 📦 Dependencies

No new dependencies added - all features built with existing packages:

- Flask for web framework
- Flask-Login for authentication
- Werkzeug for file handling and security
- SQLite for database
- Existing ML and CV libraries

### 🎨 UI/UX Improvements

- Professional gradient cards for statistics
- Responsive design for all new components
- Bootstrap modals for uploads and preferences
- Improved button layouts and spacing
- Admin panel with modern design
- Better visual feedback for actions
- Consistent color scheme throughout

### ⚡ Performance

- Efficient file upload handling
- Optimized database queries
- Lazy loading of admin data
- Client-side form validation
- Proper error handling to prevent crashes

### 🔐 Security Updates

- Password hashing for all new users
- Protected admin routes with decorators
- Secure file upload validation
- SQL injection prevention with parameterized queries
- XSS prevention in templates
- CSRF protection through Flask

---

## [1.0.0] - Initial Release

### Features

- Real-time emotion detection using webcam
- Music recommendations based on emotions
- User authentication (login/register)
- Favorites system
- User preferences
- Basic music playback
- Emotion-based filtering

### Technologies

- Flask web framework
- OpenCV for emotion detection
- SQLite database
- Bootstrap UI
- KNN recommendation algorithm

---

## Future Releases

See `PROJECT_IMPROVEMENTS.md` for planned features in upcoming versions:

- [3.0.0] Enhanced ML models for emotion detection
- [3.1.0] Playlist management system
- [3.2.0] Audio visualization
- [4.0.0] Advanced recommendation algorithms
- [4.1.0] Social features

---

**Note**: Version numbers follow [Semantic Versioning](https://semver.org/):

- MAJOR version for incompatible API changes
- MINOR version for backwards-compatible functionality additions
- PATCH version for backwards-compatible bug fixes
