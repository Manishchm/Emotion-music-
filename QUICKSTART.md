# 🚀 Quick Start Guide

Get up and running with the Emotion Music Recommender System in minutes!

## 📋 Prerequisites Checklist

Before you begin, ensure you have:

- [ ] Python 3.8 or higher installed
- [ ] Working webcam connected
- [ ] Modern web browser (Chrome, Firefox, or Edge)
- [ ] At least 500MB free disk space

## ⚡ Quick Setup (Windows)

1. **Double-click `setup.bat`**

   - This will automatically:
     - Create virtual environment
     - Install all dependencies
     - Initialize the database
     - Start the application

2. **Open your browser to:**

   ```
   http://localhost:5000
   ```

3. **Login with admin credentials:**
   - Username: `admin`
   - Password: `admin123`

That's it! You're ready to go! 🎉

## ⚡ Quick Setup (Linux/Mac)

1. **Open terminal in project folder**

2. **Make setup script executable:**

   ```bash
   chmod +x setup.sh
   ```

3. **Run setup script:**

   ```bash
   ./setup.sh
   ```

4. **Open your browser to:**
   ```
   http://localhost:5000
   ```

## 🎯 First Steps After Setup

### 1. Secure Your Admin Account

```
1. Login as admin
2. Go to Preferences
3. Change your password (recommended!)
```

### 2. Test Emotion Detection

```
1. Click "Start Camera"
2. Allow camera access
3. Click "Capture Emotion"
4. See your emotion and recommendations
```

### 3. Upload Your First Song

```
1. Click "Upload Song" button
2. Fill in song details
3. Select audio file from your device
4. Click "Upload Song"
```

### 4. Explore Admin Panel (Admin Only)

```
1. Click "Admin Panel" button
2. View system statistics
3. Manage users and songs
```

## 🔄 Running After First Setup

### Windows

```bash
# Option 1: Use run script
run.bat

# Option 2: Manual
emotion_env\Scripts\activate
python app.py
```

### Linux/Mac

```bash
# Activate environment
source emotion_env/bin/activate

# Run application
python app.py
```

## 🌐 Access Points

| Page        | URL                               | Access Level |
| ----------- | --------------------------------- | ------------ |
| Main App    | http://localhost:5000             | All Users    |
| Admin Panel | http://localhost:5000/admin/panel | Admin Only   |

## 🎵 Supported Audio Formats

When uploading songs, you can use:

- **MP3** (.mp3) - Recommended
- **WAV** (.wav)
- **OGG** (.ogg)
- **FLAC** (.flac)
- **M4A** (.m4a)

Maximum file size: **50MB**

## 📖 Quick Feature Guide

### For Regular Users

| Feature          | How to Access                  |
| ---------------- | ------------------------------ |
| Detect Emotion   | Start Camera → Capture Emotion |
| Play Songs       | Click Play button on any song  |
| Add to Favorites | Click ♥ button on songs        |
| View Favorites   | Click "Favorites" button       |
| Upload Song      | Click "Upload Song" button     |
| Set Preferences  | Click "Preferences" button     |

### For Admins

| Feature         | How to Access                      |
| --------------- | ---------------------------------- |
| Admin Panel     | Click "Admin Panel" button         |
| View Statistics | Admin Panel → Dashboard            |
| Manage Users    | Admin Panel → Users Management tab |
| Manage Songs    | Admin Panel → Songs Management tab |
| Upload Songs    | Admin Panel → Upload Song tab      |

## 🎨 Emotion Tags Guide

Choose the right emotion tag when uploading:

| Tag      | Use When Song Is              |
| -------- | ----------------------------- |
| Happy    | Upbeat, cheerful, joyful      |
| Sad      | Melancholic, slow, emotional  |
| Angry    | Aggressive, intense, powerful |
| Neutral  | Calm, ambient, balanced       |
| Surprise | Exciting, unexpected, dynamic |
| Fear     | Tense, suspenseful, dark      |

## 💡 Pro Tips

### 1. Better Emotion Detection

- Good lighting is essential
- Face the camera directly
- Remove glasses if possible
- Avoid extreme angles

### 2. Optimal Song Upload

- Use MP3 format for smaller files
- Set valence: 0.0-1.0 (sad to happy)
- Set energy: 0.0-1.0 (calm to energetic)
- Choose accurate emotion tags

### 3. Better Recommendations

- Upload diverse songs with different emotions
- Set your preferences in user settings
- Use favorites to refine future recommendations

## ❓ Common Questions

**Q: Can I use this without a camera?**
A: You can still browse, upload, and play songs, but emotion detection requires a camera.

**Q: Where are uploaded songs stored?**
A: In `static/uploads/` folder in the project directory.

**Q: Can multiple people use this?**
A: Yes! Each user has their own account with separate favorites and preferences.

**Q: Is internet required?**
A: No! This runs completely offline after setup.

**Q: Can I delete the admin account?**
A: No, but you can create additional admin accounts and change the password.

## 🆘 Having Issues?

### Camera Not Working

1. Check browser permissions
2. Try different browser
3. Restart browser
4. Check if camera works in other apps

### Songs Not Playing

1. Check file format is supported
2. Try converting to MP3
3. Check browser console for errors
4. Test with different audio file

### Database Errors

1. Delete `database/database.db`
2. Run `python database/init_database.py`
3. Restart application

### Can't Login

1. Verify you initialized database
2. Try default admin credentials
3. Check for typos in username/password
4. Clear browser cookies

## 📚 More Help

For detailed information, see:

- **README_NEW.md** - Complete documentation
- **PROJECT_IMPROVEMENTS.md** - Feature suggestions
- **CHANGELOG.md** - What's new

## 🎓 Tutorial Video (Coming Soon)

A video tutorial is planned covering:

- Complete setup walkthrough
- Feature demonstrations
- Admin panel tour
- Troubleshooting tips

## 🎉 You're All Set!

Start exploring and enjoy your emotion-based music experience!

---

**Need Help?** Open an issue on GitHub or check the documentation files.

**Found a Bug?** Please report it on the GitHub issues page.

**Have a Feature Idea?** We'd love to hear it! Submit a feature request.
