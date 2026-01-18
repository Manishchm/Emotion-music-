"""
Content-Based Filtering Algorithm
Recommends songs based on audio features similarity (valence, energy, emotion tags)
No external APIs required
"""

import sqlite3
import numpy as np

def get_content_based_recommendations(emotion, user_id=None, n_recommendations=10):
    """
    Get song recommendations using content-based filtering
    
    Args:
        emotion (str): Target emotion
        user_id (int): User ID for personalization (optional)
        n_recommendations (int): Number of songs to recommend
        
    Returns:
        list: List of recommended songs
    """
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    # Emotion to audio features mapping
    emotion_features = {
        'happy': {'valence': 0.8, 'energy': 0.7},
        'sad': {'valence': 0.2, 'energy': 0.3},
        'angry': {'valence': 0.3, 'energy': 0.9},
        'neutral': {'valence': 0.5, 'energy': 0.5},
        'surprise': {'valence': 0.7, 'energy': 0.8},
        'fear': {'valence': 0.2, 'energy': 0.6}
    }
    
    target_valence = emotion_features.get(emotion.lower(), {}).get('valence', 0.5)
    target_energy = emotion_features.get(emotion.lower(), {}).get('energy', 0.5)
    
    # Get all songs from database
    try:
        cursor.execute('''
            SELECT id, title, artist, file_path, emotion_tag, valence, energy, play_count
            FROM songs
        ''')
    except:
        # If play_count column doesn't exist, query without it
        cursor.execute('''
            SELECT id, title, artist, file_path, emotion_tag, valence, energy
            FROM songs
        ''')
    
    all_songs = cursor.fetchall()
    
    if not all_songs:
        conn.close()
        return []
    
    # Calculate similarity for each song
    song_scores = []
    
    for song_data in all_songs:
        # Handle both cases: with and without play_count
        if len(song_data) == 8:
            song_id, title, artist, file_path, emotion_tag, valence, energy, play_count = song_data
        else:
            song_id, title, artist, file_path, emotion_tag, valence, energy = song_data
            play_count = 0
        # Calculate Euclidean distance in feature space
        valence_diff = abs(valence - target_valence)
        energy_diff = abs(energy - target_energy)
        
        # Calculate feature similarity (inverse of distance)
        feature_similarity = 1 / (1 + np.sqrt(valence_diff**2 + energy_diff**2))
        
        # Boost if emotion tag matches
        emotion_boost = 1.5 if emotion_tag.lower() == emotion.lower() else 1.0
        
        # Slight boost for popular songs (but not too much)
        popularity_boost = 1 + (min(play_count, 50) / 200)  # Max 1.25x boost
        
        # Calculate final score
        score = feature_similarity * emotion_boost * popularity_boost
        
        song_scores.append({
            'id': song_id,
            'title': title,
            'artist': artist,
            'file_path': file_path,
            'emotion_tag': emotion_tag,
            'valence': valence,
            'energy': energy,
            'score': score
        })
    
    # Sort by score
    song_scores.sort(key=lambda x: x['score'], reverse=True)
    
    # Get user's listening history for diversity
    if user_id:
        cursor.execute('''
            SELECT song_id, COUNT(*) as play_count
            FROM listening_history
            WHERE user_id = ?
            GROUP BY song_id
            ORDER BY play_count DESC
        ''', (user_id,))
        
        user_history = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Penalize recently played songs (but don't exclude them)
        for song in song_scores:
            if song['id'] in user_history:
                played_count = user_history[song['id']]
                penalty = 1 - (min(played_count, 10) / 40)  # Max 25% penalty
                song['score'] *= penalty
        
        # Re-sort after applying penalties
        song_scores.sort(key=lambda x: x['score'], reverse=True)
    
    conn.close()
    
    # Return top N recommendations
    return song_scores[:n_recommendations]


def get_similar_songs(song_id, n_recommendations=5):
    """
    Find songs similar to a given song
    
    Args:
        song_id (int): ID of the reference song
        n_recommendations (int): Number of similar songs to return
        
    Returns:
        list: List of similar songs
    """
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    # Get the reference song
    cursor.execute('''
        SELECT id, title, artist, file_path, emotion_tag, valence, energy
        FROM songs
        WHERE id = ?
    ''', (song_id,))
    
    reference_song = cursor.fetchone()
    
    if not reference_song:
        conn.close()
        return []
    
    ref_id, ref_title, ref_artist, ref_path, ref_emotion, ref_valence, ref_energy = reference_song
    
    # Get all other songs
    cursor.execute('''
        SELECT id, title, artist, file_path, emotion_tag, valence, energy
        FROM songs
        WHERE id != ?
    ''', (song_id,))
    
    all_songs = cursor.fetchall()
    
    if not all_songs:
        conn.close()
        return []
    
    # Calculate similarity
    similar_songs = []
    
    for song_id, title, artist, file_path, emotion_tag, valence, energy in all_songs:
        # Calculate feature distance
        valence_diff = abs(valence - ref_valence)
        energy_diff = abs(energy - ref_energy)
        
        # Feature similarity
        similarity = 1 / (1 + np.sqrt(valence_diff**2 + energy_diff**2))
        
        # Boost if same emotion
        if emotion_tag.lower() == ref_emotion.lower():
            similarity *= 1.3
        
        # Boost if same artist  
        if artist.lower() == ref_artist.lower():
            similarity *= 1.2
        
        similar_songs.append({
            'id': song_id,
            'title': title,
            'artist': artist,
            'file_path': file_path,
            'emotion_tag': emotion_tag,
            'similarity': similarity
        })
    
    # Sort by similarity
    similar_songs.sort(key=lambda x: x['similarity'], reverse=True)
    
    conn.close()
    
    return similar_songs[:n_recommendations]


if __name__ == '__main__':
    # Test the content-based filtering
    print("Testing Content-Based Filtering...")
    
    recommendations = get_content_based_recommendations('happy', n_recommendations=5)
    
    if recommendations:
        print(f"\nTop 5 recommendations for 'happy' emotion:")
        for i, song in enumerate(recommendations, 1):
            print(f"{i}. {song['title']} by {song['artist']} (score: {song['score']:.3f})")
    else:
        print("No songs in database. Please add some songs first.")
