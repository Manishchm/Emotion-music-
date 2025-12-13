"""
Hybrid Recommendation Algorithm
Combines KNN-based and Content-Based filtering for better recommendations
No external APIs required
"""

import sqlite3
import sys
import os

# Add parent directory to path to import other modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_model.recommendation_engine import get_recommendations as knn_recommendations
from ml_model.content_based_filter import get_content_based_recommendations

def get_hybrid_recommendations(emotion, user_id=None, n_recommendations=10):
    """
    Get song recommendations using hybrid approach (KNN + Content-Based)
    
    Args:
        emotion (str): Target emotion
        user_id (int): User ID for personalization (optional)
        n_recommendations (int): Number of songs to recommend
        
    Returns:
        list: List of recommended songs with diversity
    """
    
    # Get recommendations from both algorithms
    try:
        # KNN recommendations (existing algorithm)
        knn_results = knn_recommendations(emotion, limit=n_recommendations * 2)
    except Exception as e:
        print(f"KNN algorithm error: {e}")
        knn_results = []
    
    try:
        # Content-based recommendations
        content_results = get_content_based_recommendations(
            emotion, 
            user_id=user_id, 
            n_recommendations=n_recommendations * 2
        )
    except Exception as e:
        print(f"Content-based algorithm error: {e}")
        content_results = []
    
    # If one algorithm fails, use the other
    if not knn_results and not content_results:
        return []
    elif not knn_results:
        return content_results[:n_recommendations]
    elif not content_results:
        return knn_results[:n_recommendations]
    
    # Combine results using weighted scoring
    combined_scores = {}
    
    # Process KNN results (weight: 0.4)
    knn_weight = 0.4
    for i, song in enumerate(knn_results):
        song_id = song.get('id')
        if song_id:
            # Score based on ranking (higher rank = higher score)
            rank_score = (len(knn_results) - i) / len(knn_results)
            combined_scores[song_id] = {
                'song': song,
                'score': rank_score * knn_weight,
                'sources': ['knn']
            }
    
    # Process Content-Based results (weight: 0.6)
    content_weight = 0.6
    for i, song in enumerate(content_results):
        song_id = song.get('id')
        if song_id:
            # Use the similarity score from content-based filtering
            content_score = song.get('score', 0)
            
            if song_id in combined_scores:
                # Song appears in both - boost its score
                combined_scores[song_id]['score'] += content_score * content_weight
                combined_scores[song_id]['sources'].append('content')
            else:
                combined_scores[song_id] = {
                    'song': song,
                    'score': content_score * content_weight,
                    'sources': ['content']
                }
    
    # Boost songs that appear in both algorithms
    for song_id in combined_scores:
        if len(combined_scores[song_id]['sources']) > 1:
            combined_scores[song_id]['score'] *= 1.3  # 30% boost for consensus
    
    # Convert to list and sort by score
    final_recommendations = []
    for song_id, data in combined_scores.items():
        song = data['song']
        song['hybrid_score'] = data['score']
        song['recommendation_sources'] = data['sources']
        final_recommendations.append(song)
    
    # Sort by hybrid score
    final_recommendations.sort(key=lambda x: x['hybrid_score'], reverse=True)
    
    # Add diversity - avoid too many songs from same artist
    diverse_recommendations = []
    artist_count = {}
    
    for song in final_recommendations:
        artist = song.get('artist', 'Unknown')
        
        # Limit songs per artist (max 2 in top results)
        if artist_count.get(artist, 0) < 2:
            diverse_recommendations.append(song)
            artist_count[artist] = artist_count.get(artist, 0) + 1
        else:
            # Still add but with lower priority if we have space
            if len(diverse_recommendations) >= n_recommendations:
                continue
            diverse_recommendations.append(song)
        
        if len(diverse_recommendations) >= n_recommendations:
            break
    
    # If we still need more songs, add the rest
    if len(diverse_recommendations) < n_recommendations:
        for song in final_recommendations:
            if song not in diverse_recommendations:
                diverse_recommendations.append(song)
                if len(diverse_recommendations) >= n_recommendations:
                    break
    
    return diverse_recommendations[:n_recommendations]


def get_personalized_recommendations(user_id, emotion, n_recommendations=10):
    """
    Get personalized recommendations based on user's history
    
    Args:
        user_id (int): User ID
        emotion (str): Current emotion
        n_recommendations (int): Number of recommendations
        
    Returns:
        list: Personalized song recommendations
    """
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    
    # Get user's favorite genres and artists from preferences
    cursor.execute('''
        SELECT preferred_genre, preferred_artist
        FROM user_preferences
        WHERE user_id = ?
    ''', (user_id,))
    
    preferences = cursor.fetchone()
    preferred_genre = preferences[0] if preferences and preferences[0] else None
    preferred_artist = preferences[1] if preferences and preferences[1] else None
    
    # Get user's most played emotions
    cursor.execute('''
        SELECT emotion, COUNT(*) as count
        FROM emotion_history
        WHERE user_id = ?
        GROUP BY emotion
        ORDER BY count DESC
        LIMIT 3
    ''', (user_id,))
    
    favorite_emotions = [row[0] for row in cursor.fetchall()]
    
    # Get user's most played songs
    cursor.execute('''
        SELECT s.id, s.emotion_tag, COUNT(*) as play_count
        FROM listening_history lh
        JOIN songs s ON lh.song_id = s.id
        WHERE lh.user_id = ?
        GROUP BY s.id
        ORDER BY play_count DESC
        LIMIT 10
    ''', (user_id,))
    
    favorite_songs = cursor.fetchall()
    conn.close()
    
    # Get hybrid recommendations
    recommendations = get_hybrid_recommendations(emotion, user_id, n_recommendations * 2)
    
    # Apply personalization boost
    for song in recommendations:
        boost = 1.0
        
        # Boost if matches user's preferred artist
        if preferred_artist and song.get('artist', '').lower() == preferred_artist.lower():
            boost *= 1.4
        
        # Boost if emotion is one of user's favorites
        if song.get('emotion_tag', '').lower() in [e.lower() for e in favorite_emotions]:
            boost *= 1.2
        
        # Apply boost to score
        if 'hybrid_score' in song:
            song['hybrid_score'] *= boost
    
    # Re-sort after personalization
    recommendations.sort(key=lambda x: x.get('hybrid_score', 0), reverse=True)
    
    return recommendations[:n_recommendations]


if __name__ == '__main__':
    # Test the hybrid recommender
    print("Testing Hybrid Recommendation System...")
    
    recommendations = get_hybrid_recommendations('happy', n_recommendations=5)
    
    if recommendations:
        print(f"\nTop 5 hybrid recommendations for 'happy' emotion:")
        for i, song in enumerate(recommendations, 1):
            sources = ', '.join(song.get('recommendation_sources', []))
            score = song.get('hybrid_score', 0)
            print(f"{i}. {song['title']} by {song['artist']}")
            print(f"   Score: {score:.3f}, Sources: [{sources}]")
    else:
        print("No songs in database. Please add some songs first.")
