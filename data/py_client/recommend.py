import requests
from . import playlists, top_items

def get_trackSeeds(access_token):
    short_tracks = top_items.topTracks(access_token, limit=5, time_range="short_term")
    medium_tracks = top_items.topTracks(access_token, limit=5, time_range="medium_term")
    long_tracks = top_items.topTracks(access_token, limit=5, time_range="long_term")


    shortTrackIds = [track["song_id"] for track in short_tracks]
    mediumTrackIds = [track["song_id"] for track in medium_tracks]
    longTrackIds = [track["song_id"] for track in long_tracks]

    seeds = {
        "short_term": ','.join(shortTrackIds),
        "medium_term": ','.join(mediumTrackIds),
        "long_term": ','.join(longTrackIds),
    }

    return seeds


def get_recommendTracks(access_token, trackSeeds):

    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url = f"https://api.spotify.com/v1/recommendations?seed_tracks={trackSeeds}&limit=5"

    response = requests.get(url, headers=headers)

    json_data = response.json()

    all_tracks = []

    for item in json_data["tracks"]:
        track = {}
        track["song_name"] = item["name"]
        track["song_id"] = item["id"]
        track["song_url"] = item["external_urls"]["spotify"]
        track["song_image"] = None if item["album"]["images"] == [] else item["album"]["images"][-1]["url"]
        track["singer_names"] = [name["name"] for name in item["artists"]]

        all_tracks.append(track)
    
    return all_tracks




def track_recommend(access_token):

    allTrackSeeds = get_trackSeeds(access_token)

    shortTremSeeds = allTrackSeeds["short_term"]
    shortTremRecommend = get_recommendTracks(access_token, shortTremSeeds)

    mediumTremSeeds = allTrackSeeds["medium_term"]
    mediumTremRecommend = get_recommendTracks(access_token, mediumTremSeeds)

    
    longTremSeeds = allTrackSeeds["long_term"]
    longTremRecommend = get_recommendTracks(access_token, longTremSeeds)
    
    recommendations = {
        "short_term": shortTremRecommend,
        "medium_term": mediumTremRecommend,
        "long_term": longTremRecommend
    }

    return recommendations