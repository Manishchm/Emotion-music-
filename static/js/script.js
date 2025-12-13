// Global variables
let videoStream = null;
let isCameraOn = false;
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureBtn = document.getElementById('capture-btn');
const startCamBtn = document.getElementById('start-cam');
const stopCamBtn = document.getElementById('stop-cam');
const emotionLabel = document.getElementById('emotion-label');
const confidenceElement = document.getElementById('confidence');
const songList = document.getElementById('song-list');
const noRecommendations = document.getElementById('no-recommendations');
const audioPlayer = document.getElementById('audio-player');
const nowPlaying = document.getElementById('now-playing');
const refreshBtn = document.getElementById('refresh-btn');
const authSection = document.getElementById('auth-section');
const userSection = document.getElementById('user-section');
const appSection = document.getElementById('app-section');
const favoritesSection = document.getElementById('favorites-section');
const userName = document.getElementById('user-name');
const userEmail = document.getElementById('user-email');
const logoutBtn = document.getElementById('logout-btn');
const favoritesBtn = document.getElementById('favorites-btn');
const preferencesBtn = document.getElementById('preferences-btn');
const favoritesList = document.getElementById('favorites-list');
const noFavorites = document.getElementById('no-favorites');
const adminPanelBtn = document.getElementById('admin-panel-btn');
const submitUploadBtn = document.getElementById('submit-upload');

// Initialize
document.addEventListener('DOMContentLoaded', function () {
    // Set up event listeners
    startCamBtn.addEventListener('click', startCamera);
    stopCamBtn.addEventListener('click', stopCamera);
    captureBtn.addEventListener('click', captureEmotion);
    refreshBtn.addEventListener('click', refreshRecommendations);
    logoutBtn.addEventListener('click', logout);
    favoritesBtn.addEventListener('click', showFavorites);
    preferencesBtn.addEventListener('click', showPreferences);
    document.getElementById('save-preferences').addEventListener('click', savePreferences);

    // Set up form submissions
    document.getElementById('login-form').addEventListener('submit', login);
    document.getElementById('register-form').addEventListener('submit', register);

    // Set up upload button
    if (submitUploadBtn) {
        submitUploadBtn.addEventListener('click', uploadSong);
    }

    // Set up admin panel button
    if (adminPanelBtn) {
        adminPanelBtn.addEventListener('click', function () {
            window.location.href = '/admin/panel';
        });
    }

    // Initially disable capture button
    captureBtn.disabled = true;
    stopCamBtn.disabled = true;

    // Check if user is already logged in
    checkLoginStatus();
});

// Check if user is logged in
function checkLoginStatus() {
    fetch('/user_info')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showUserSection(data.user);
            } else {
                showAuthSection();
            }
        })
        .catch(error => {
            console.error('Error checking login status:', error);
            showAuthSection();
        });
}

// Show authentication section
function showAuthSection() {
    authSection.classList.remove('d-none');
    userSection.classList.add('d-none');
    appSection.classList.add('d-none');
    favoritesSection.classList.add('d-none');
}

// Show user section
function showUserSection(user) {
    authSection.classList.add('d-none');
    userSection.classList.remove('d-none');

    // Show dashboard by default
    const dashboardSection = document.getElementById('dashboard-section');
    if (dashboardSection) {
        dashboardSection.classList.remove('d-none');
    }

    // Hide other sections initially
    appSection.classList.add('d-none');
    favoritesSection.classList.add('d-none');

    userName.textContent = user.username;
    userEmail.textContent = user.email;

    // Show admin panel button if user is admin
    if (user.is_admin) {
        adminPanelBtn.classList.remove('d-none');
    } else {
        adminPanelBtn.classList.add('d-none');
    }

    // Load user preferences
    loadPreferences();

    // Initialize dashboard with analytics
    setTimeout(() => {
        if (typeof initDashboard === 'function') {
            initDashboard();
        }
    }, 500);
}

// Login function
function login(event) {
    event.preventDefault();

    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                checkLoginStatus();
            } else {
                alert('Login failed: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Login failed. Please try again.');
        });
}

// Register function
function register(event) {
    event.preventDefault();

    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, email, password })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Registration successful. Please login.');
                document.getElementById('login-tab').click();
            } else {
                alert('Registration failed: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Registration failed. Please try again.');
        });
}

// Logout function
function logout() {
    fetch('/logout')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAuthSection();
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Show favorites
function showFavorites() {
    appSection.classList.add('d-none');
    favoritesSection.classList.remove('d-none');

    fetch('/get_favorites')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayFavorites(data.favorites);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Display favorites
function displayFavorites(favorites) {
    favoritesList.innerHTML = '';

    if (favorites.length === 0) {
        noFavorites.classList.remove('d-none');
        return;
    }

    noFavorites.classList.add('d-none');

    favorites.forEach(song => {
        const listItem = document.createElement('li');
        listItem.className = 'list-group-item d-flex justify-content-between align-items-center';
        listItem.innerHTML = `
            <div>
                <strong>${song.title}</strong><br>
                <small class="text-muted">${song.artist}</small>
            </div>
            <div>
                <button class="btn btn-sm btn-outline-primary play-btn me-2" data-path="${song.file_path}">
                    Play
                </button>
                <button class="btn btn-sm btn-outline-danger remove-favorite-btn" data-id="${song.id}">
                    Remove
                </button>
            </div>
        `;

        favoritesList.appendChild(listItem);
    });

    // Add event listeners
    document.querySelectorAll('.play-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const songPath = this.getAttribute('data-path');
            playSong(songPath, this);
        });
    });

    document.querySelectorAll('.remove-favorite-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const songId = this.getAttribute('data-id');
            removeFavorite(songId, this.closest('li'));
        });
    });
}

// Remove favorite
function removeFavorite(songId, listItem) {
    fetch('/remove_favorite', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ song_id: songId })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                listItem.remove();

                // Check if there are any favorites left
                if (favoritesList.children.length === 0) {
                    noFavorites.classList.remove('d-none');
                }
            } else {
                alert('Failed to remove favorite: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to remove favorite. Please try again.');
        });
}

// Show preferences modal
function showPreferences() {
    const modal = new bootstrap.Modal(document.getElementById('preferencesModal'));
    modal.show();
}

// Load preferences
function loadPreferences() {
    fetch('/get_preferences')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('preferred-genre').value = data.preferences.preferred_genre || '';
                document.getElementById('preferred-artist').value = data.preferences.preferred_artist || '';
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Save preferences
function savePreferences() {
    const preferredGenre = document.getElementById('preferred-genre').value;
    const preferredArtist = document.getElementById('preferred-artist').value;

    fetch('/save_preferences', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            preferred_genre: preferredGenre,
            preferred_artist: preferredArtist
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Preferences saved successfully!');
                bootstrap.Modal.getInstance(document.getElementById('preferencesModal')).hide();
            } else {
                alert('Failed to save preferences: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to save preferences. Please try again.');
        });
}

// Refresh recommendations
function refreshRecommendations() {
    if (emotionLabel.textContent !== 'None') {
        getRecommendations(emotionLabel.textContent);
    }
}

// Start camera
async function startCamera() {
    try {
        videoStream = await navigator.mediaDevices.getUserMedia({
            video: { width: 640, height: 480 }
        });
        video.srcObject = videoStream;
        isCameraOn = true;

        // Enable/disable buttons
        captureBtn.disabled = false;
        stopCamBtn.disabled = false;
        startCamBtn.disabled = true;
    } catch (err) {
        console.error('Error accessing camera:', err);
        alert('Could not access camera. Please check permissions.');
    }
}

// Stop camera
function stopCamera() {
    if (videoStream) {
        videoStream.getTracks().forEach(track => track.stop());
        video.srcObject = null;
        isCameraOn = false;

        // Enable/disable buttons
        captureBtn.disabled = true;
        stopCamBtn.disabled = true;
        startCamBtn.disabled = false;

        // Reset emotion label
        emotionLabel.textContent = 'None';
        confidenceElement.textContent = '0%';
    }
}

// Capture emotion from camera
function captureEmotion() {
    if (!isCameraOn) {
        alert('Please start the camera first.');
        return;
    }

    // Draw video frame to canvas
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert canvas to base64
    const imageData = canvas.toDataURL('image/jpeg');

    // Send to server for emotion analysis
    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: imageData })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update emotion label
                emotionLabel.textContent = data.emotion;
                emotionLabel.className = `badge bg-${getEmotionColor(data.emotion)}`;
                confidenceElement.textContent = `${(data.confidence * 100).toFixed(2)}%`;

                // Get music recommendations
                getRecommendations(data.emotion);
            } else {
                console.error('Error analyzing emotion:', data.error);
                alert('Error analyzing emotion. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error analyzing emotion. Please try again.');
        });
}

// Get music recommendations based on emotion
function getRecommendations(emotion) {
    fetch('/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ emotion: emotion })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayRecommendations(data.songs);
            } else {
                console.error('Error getting recommendations:', data.error);
                alert('Error getting recommendations. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error getting recommendations. Please try again.');
        });
}


// Display recommendations
function displayRecommendations(songs) {
    // Clear previous recommendations
    songList.innerHTML = '';
    noRecommendations.classList.add('d-none');

    if (songs.length === 0) {
        noRecommendations.textContent = 'No recommendations found for this emotion.';
        noRecommendations.classList.remove('d-none');
        return;
    }

    // Add each song to the list
    songs.forEach(song => {
        const listItem = document.createElement('li');
        listItem.className = 'list-group-item d-flex justify-content-between align-items-center fade-in';
        listItem.innerHTML = `
            <div>
                <strong>${song.title}</strong><br>
                <small class="text-muted">${song.artist}</small>
            </div>
            <div>
                <button class="btn btn-sm btn-outline-primary play-btn me-2" data-id="${song.id}" data-path="${song.file_path}" data-title="${song.title}" data-artist="${song.artist}">
                    ▶ Play
                </button>
                <button class="btn btn-sm btn-outline-success favorite-btn" data-id="${song.id}">
                    ♥
                </button>
            </div>
        `;

        songList.appendChild(listItem);
    });

    // Add event listeners to play buttons
    document.querySelectorAll('.play-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const songId = this.getAttribute('data-id');
            const songPath = this.getAttribute('data-path');
            const songTitle = this.getAttribute('data-title');
            const songArtist = this.getAttribute('data-artist');
            playSongEnhanced(songId, songPath, songTitle, songArtist);
        });
    });

    // Add event listeners to favorite buttons
    document.querySelectorAll('.favorite-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const songId = this.getAttribute('data-id');
            addFavorite(songId, this);
        });
    });
}

// Add to favorites
function addFavorite(songId, button) {
    fetch('/add_favorite', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ song_id: songId })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                button.classList.remove('btn-outline-success');
                button.classList.add('btn-success');
                button.disabled = true;
                button.textContent = '✓';
            } else {
                alert('Failed to add to favorites: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to add to favorites. Please try again.');
        });
}

// Play a song
function playSong(songPath, button) {
    // Update now playing text
    const songItem = button.closest('.list-group-item');
    const songTitle = songItem.querySelector('strong').textContent;
    const artistName = songItem.querySelector('.text-muted').textContent;
    nowPlaying.textContent = `${songTitle} by ${artistName}`;

    // Set audio source and play
    audioPlayer.src = songPath;
    audioPlayer.play();

    // Visual feedback
    document.querySelectorAll('.play-btn').forEach(btn => {
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-outline-primary');
    });

    button.classList.remove('btn-outline-primary');
    button.classList.add('btn-primary');
}

// Helper function to get color based on emotion
function getEmotionColor(emotion) {
    const colorMap = {
        'happy': 'success',
        'sad': 'info',
        'angry': 'danger',
        'surprise': 'warning',
        'neutral': 'secondary',
        'fear': 'dark',
        'disgust': 'dark'
    };

    return colorMap[emotion.toLowerCase()] || 'primary';
}

// Upload song function
function uploadSong() {
    const form = document.getElementById('upload-form');
    const formData = new FormData();

    const title = document.getElementById('song-title').value;
    const artist = document.getElementById('song-artist').value;
    const emotionTag = document.getElementById('song-emotion').value;
    const valence = document.getElementById('song-valence').value;
    const energy = document.getElementById('song-energy').value;
    const audioFile = document.getElementById('audio-file').files[0];

    if (!title || !artist || !emotionTag || !audioFile) {
        alert('Please fill in all required fields');
        return;
    }

    formData.append('title', title);
    formData.append('artist', artist);
    formData.append('emotion_tag', emotionTag);
    formData.append('valence', valence);
    formData.append('energy', energy);
    formData.append('audio_file', audioFile);

    const statusDiv = document.getElementById('upload-status');
    statusDiv.innerHTML = '<div class="alert alert-info">Uploading...</div>';
    submitUploadBtn.disabled = true;

    fetch('/upload_song', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                statusDiv.innerHTML = '<div class="alert alert-success">' + data.message + '</div>';
                form.reset();
                setTimeout(() => {
                    bootstrap.Modal.getInstance(document.getElementById('uploadModal')).hide();
                    statusDiv.innerHTML = '';
                }, 2000);
            } else {
                statusDiv.innerHTML = '<div class="alert alert-danger">' + data.message + '</div>';
            }
            submitUploadBtn.disabled = false;
        })
        .catch(error => {
            console.error('Error:', error);
            statusDiv.innerHTML = '<div class="alert alert-danger">Error uploading song. Please try again.</div>';
            submitUploadBtn.disabled = false;
        });
}

// ===== NEW FEATURES =====

// Track song play
function trackSongPlay(songId) {
    fetch('/track_play', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ song_id: songId })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Play tracked successfully');
            }
        })
        .catch(error => {
            console.error('Error tracking play:', error);
        });
}

// Enhanced play song function with tracking
function playSongEnhanced(songId, songPath, songTitle, artistName) {
    // Update now playing
    nowPlaying.textContent = `${songTitle} by ${artistName}`;

    // Set audio source and play
    audioPlayer.src = songPath;
    audioPlayer.play();

    // Track the play
    trackSongPlay(songId);

    // Visual feedback
    document.querySelectorAll('.play-btn').forEach(btn => {
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-outline-primary');
    });

    // Highlight currently playing song
    const currentBtn = document.querySelector(`[data-id="${songId}"].play-btn`);
    if (currentBtn) {
        currentBtn.classList.remove('btn-outline-primary');
        currentBtn.classList.add('btn-primary');
    }

    showToast('Now Playing', `${songTitle} by ${artistName}`, 'info');
}

// Load emotion history
function loadEmotionHistory(limit = 20) {
    fetch(`/emotion_history?limit=${limit}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayEmotionHistory(data.history);
            }
        })
        .catch(error => {
            console.error('Error loading emotion history:', error);
        });
}

// Display emotion history
function displayEmotionHistory(history) {
    const container = document.getElementById('emotion-history-list');

    if (!container) return;

    if (history.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">😐</div>
                <div class="empty-state-text">No emotion history yet. Capture your first emotion!</div>
            </div>
        `;
        return;
    }

    let html = '<div class="timeline">';

    history.forEach(item => {
        const emotionColor = getEmotionColor(item.emotion);
        const date = new Date(item.timestamp);
        const timeStr = date.toLocaleString();

        html += `
            <div class="timeline-item fade-in">
                <div class="timeline-marker"></div>
                <div class="timeline-content">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <span class="badge bg-${emotionColor}">${item.emotion.toUpperCase()}</span>
                            <small class="text-muted ms-2">${(item.confidence * 100).toFixed(1)}% confidence</small>
                        </div>
                        <small class="text-muted">${timeStr}</small>
                    </div>
                </div>
            </div>
        `;
    });

    html += '</div>';
    container.innerHTML = html;
}

// Load listening history
function loadListeningHistory(limit = 20) {
    fetch(`/listening_history?limit=${limit}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayListeningHistory(data.history);
            }
        })
        .catch(error => {
            console.error('Error loading listening history:', error);
        });
}

// Display listening history
function displayListeningHistory(history) {
    const container = document.getElementById('listening-history-list');

    if (!container) return;

    if (history.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🎵</div>
                <div class="empty-state-text">No listening history yet. Play your first song!</div>
            </div>
        `;
        return;
    }

    let html = '<ul class="list-group">';

    history.forEach(item => {
        const date = new Date(item.timestamp);
        const timeStr = date.toLocaleString();

        html += `
            <li class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                    <strong>${item.title}</strong><br>
                    <small class="text-muted">${item.artist} • ${item.emotion_tag}</small><br>
                    <small class="text-muted">${timeStr}</small>
                </div>
                <button class="btn btn-sm btn-outline-primary play-btn" 
                        onclick="playSongEnhanced(${item.id}, '${item.file_path}', '${item.title}', '${item.artist}')">
                    ▶ Play
                </button>
            </li>
        `;
    });

    html += '</ul>';
    container.innerHTML = html;
}

// Load most played songs
function loadMostPlayed(limit = 10) {
    fetch(`/most_played?limit=${limit}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayMostPlayed(data.songs);
            }
        })
        .catch(error => {
            console.error('Error loading most played:', error);
        });
}

// Display most played songs
function displayMostPlayed(songs) {
    const container = document.getElementById('most-played-list');

    if (!container) return;

    if (songs.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🎧</div>
                <div class="empty-state-text">No songs played yet!</div>
            </div>
        `;
        return;
    }

    let html = '<ul class="list-group">';

    songs.forEach((song, index) => {
        html += `
            <li class="list-group-item d-flex justify-content-between align-items-center">
                <div class="flex-grow-1">
                    <span class="badge bg-${index < 3 ? 'primary' : 'secondary'} me-2">#${index + 1}</span>
                    <strong>${song.title}</strong><br>
                    <small class="text-muted">${song.artist}</small>
                </div>
                <div class="text-end">
                    <span class="badge bg-info">${song.play_count} plays</span><br>
                    <button class="btn btn-sm btn-outline-primary play-btn mt-1" 
                            onclick="playSongEnhanced(${song.id}, '${song.file_path}', '${song.title}', '${song.artist}')">
                        ▶
                    </button>
                </div>
            </li>
        `;
    });

    html += '</ul>';
    container.innerHTML = html;
}

// Load emotion stats
function loadEmotionStats() {
    fetch('/emotion_stats')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayEmotionStats(data.stats);
            }
        })
        .catch(error => {
            console.error('Error loading emotion stats:', error);
        });
}

// Display emotion stats
function displayEmotionStats(stats) {
    const container = document.getElementById('emotion-stats-container');

    if (!container) return;

    // Update total captures
    const totalElement = document.getElementById('total-captures');
    if (totalElement) {
        totalElement.textContent = stats.total_captures || 0;
    }

    // Display distribution
    if (stats.distribution && stats.distribution.length > 0) {
        let html = '';

        stats.distribution.forEach(item => {
            const percentage = stats.total_captures > 0
                ? ((item.count / stats.total_captures) * 100).toFixed(1)
                : 0;
            const emotionColor = getEmotionColor(item.emotion);

            html += `
                <div class="mb-3">
                    <div class="d-flex justify-content-between mb-1">
                        <span class="badge bg-${emotionColor}">${item.emotion.toUpperCase()}</span>
                        <span class="text-muted">${item.count} (${percentage}%)</span>
                    </div>
                    <div class="progress">
                        <div class="progress-bar" style="width: ${percentage}%"></div>
                    </div>
                </div>
            `;
        });

        container.innerHTML = html;
    } else {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-text">No emotion data yet</div>
            </div>
        `;
    }
}

// Show toast notification
function showToast(title, message, type = 'info') {
    const toastContainer = document.getElementById('toast-container');

    if (!toastContainer) {
        // Create toast container if it doesn't exist
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const toastId = 'toast-' + Date.now();
    const bgClass = type === 'success' ? 'bg-success' : type === 'error' ? 'bg-danger' : 'bg-info';

    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white ${bgClass} border-0 fade show" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <strong>${title}</strong><br>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" onclick="document.getElementById('${toastId}').remove()"></button>
            </div>
        </div>
    `;

    document.getElementById('toast-container').insertAdjacentHTML('beforeend', toastHTML);

    // Auto-remove after 4 seconds
    setTimeout(() => {
        const toast = document.getElementById(toastId);
        if (toast) {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }
    }, 4000);
}

// Show loading overlay
function showLoading() {
    const overlay = document.createElement('div');
    overlay.id = 'loading-overlay';
    overlay.className = 'loading-overlay';
    overlay.innerHTML = '<div class="spinner"></div>';
    document.body.appendChild(overlay);
}

// Hide loading overlay
function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.remove();
    }
}

// Initialize dashboard when user section is shown
function initDashboard() {
    // Load all data
    loadEmotionHistory(20);
    loadListeningHistory(20);
    loadMostPlayed(10);
    loadEmotionStats();
}

// Navigation functions
function showDashboard() {
    hideAllSections();
    document.getElementById('dashboard-section').classList.remove('d-none');
    initDashboard();
}

function showEmotionDetection() {
    hideAllSections();
    const appSection = document.getElementById('app-section');
    if (appSection) {
        appSection.classList.remove('d-none');
    }
}

function hideAllSections() {
    const dashboardSection = document.getElementById('dashboard-section');
    const appSection = document.getElementById('app-section');
    const favoritesSection = document.getElementById('favorites-section');

    if (dashboardSection) dashboardSection.classList.add('d-none');
    if (appSection) appSection.classList.add('d-none');
    if (favoritesSection) favoritesSection.classList.add('d-none');
}
