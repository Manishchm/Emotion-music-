import sqlite3
import numpy as np
import os

# Map emotions to target valence and energy values
EMOTION_FEATURE_MAP = {
    'angry': [0.3, 0.9],
    'disgust': [0.3, 0.4],
    'fear': [0.2, 0.6],
    'happy': [0.8, 0.7],
    'sad': [0.2, 0.3],
    'surprise': [0.7, 0.8],
    'neutral': [0.5, 0.5]
}

def get_song_features():
    """Retrieve all songs and their features from the database"""
    try:
        conn = sqlite3.connect('database/database.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, title, artist, file_path, valence, energy FROM songs')
        songs = cursor.fetchall()
        
        conn.close()
        
        # Extract features
        song_ids = [song[0] for song in songs]
        features = np.array([[song[4], song[5]] for song in songs])
        song_info = [{
            'id': song[0],
            'title': song[1],
            'artist': song[2],
            'file_path': song[3]
        } for song in songs]
        
        return song_ids, features, song_info
    except:
        # Return empty values if database is not available
        return [], np.array([]), []

def get_recommendations(target_emotion, n_recommendations=5, limit=None):
    """Get song recommendations based on target emotion"""
    # Handle limit parameter for backwards compatibility
    if limit is not None:
        n_recommendations = limit
        
    # Get target features for the emotion
    target_features = EMOTION_FEATURE_MAP.get(target_emotion.lower(), [0.5, 0.5])
    
    # Get all songs and their features
    song_ids, features, song_info = get_song_features()
    
    if len(features) == 0:
        # Return some default recommendations if no songs in database
        return [{
            'id': i,
            'title': f'Sample {target_emotion.capitalize()} Song {i}',
            'artist': 'Sample Artist',
            'file_path': f'/static/music/{target_emotion}/sample{i}.mp3'
        } for i in range(1, 6)]
    
    # Calculate distances manually using numpy
    target_array = np.array(target_features)
    distances = np.sqrt(np.sum((features - target_array) ** 2, axis=1))
    
    # Get indices of n_recommendations closest songs
    n_recs = min(n_recommendations, len(features))
    indices = np.argsort(distances)[:n_recs]
    
    # Get recommended songs
    recommendations = []
    for idx in indices:
        recommendations.append(song_info[idx])
    
    return recommendations

if __name__ == '__main__':
    # Test the recommendation system
    recommendations = get_recommendations('happy')
    print("Recommendations for 'happy':")
    for song in recommendations:
        print(f"- {song['title']} by {song['artist']}")