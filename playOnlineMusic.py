import requests
import json

def search_and_play(query):
    query = query.replace(" ", "+")
    url = "https://www.googleapis.com/youtube/v3/search?part=snippet&q={}&type=video&key={YOUR_API_KEY}".format(query)
    response = requests.get(url)
    results = json.loads(response.text)
    video_id = results['items'][0]['id']['videoId']
    video_url = "https://www.youtube.com/watch?v={}".format(video_id)
    # use a library like vlc to play the video
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(video_url)
    player.set_media(media)
    player.play()