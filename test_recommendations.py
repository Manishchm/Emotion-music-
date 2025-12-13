import requests

print("\n" + "="*60)
print("🎵 TESTING EMOTION-BASED MUSIC RECOMMENDATIONS")
print("="*60 + "\n")

emotions = ['happy', 'sad', 'angry', 'neutral', 'surprise', 'fear']

for emotion in emotions:
    response = requests.post('http://localhost:5000/recommend', json={'emotion': emotion})
    result = response.json()
    
    if result.get('success'):
        songs = result.get('songs', [])
        print(f"😊 {emotion.upper()}: {len(songs)} songs")
        for i, song in enumerate(songs[:3], 1):
            print(f"   {i}. {song['title']} - {song['artist']}")
    else:
        print(f"❌ {emotion}: Failed")
    print()

print("="*60)
print("✅ All emotion recommendations tested!")
print("="*60)
