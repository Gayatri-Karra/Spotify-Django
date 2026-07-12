import requests
from django.conf import settings

def topItems(access_token, time_range, item, limit):
    if time_range == None:
        time_range = 'medium_term'
        
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url = f"https://api.spotify.com/v1/me/top/{item}?time_range={time_range}&limit={limit}"

    response = requests.get(url, headers=headers)

    return response


def topTracks(access_token, time_range, limit=50):

    response = topItems(access_token, time_range, "tracks", limit)

    if response.status_code == 401:
        return 401

    json_data = response.json()

    all_tracks = []

    for item in json_data["items"]:
        track = {}
        track["song_name"] = item["name"]
        track["song_id"] = item["id"]
        track["song_url"] = item["external_urls"]["spotify"]
        track["song_image"] = None if item["album"]["images"] == [] else item["album"]["images"][-1]["url"]
        track["singer_names"] = [name["name"] for name in item["artists"]]

        all_tracks.append(track)
    
    return all_tracks



def topArtists(access_token, time_range, limit=50):

    response = topItems(access_token, time_range, "artists", limit)

    if response.status_code == 401:
        return None
    
    json_data = response.json()

    all_artists = []

    for item in json_data["items"]:
        track = {}
        track["artist_name"] = item["name"]
        track["artist_id"] = item["id"]
        track["artist_genres"] = item["genres"]
        track["artist_url"] = item["external_urls"]["spotify"]
        track["artist_image"] = "" if item["images"] == [] else item["images"][0]["url"]

        all_artists.append(track)
    
    return all_artists


class TopItems:
    
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://api.spotify.com/v1/me/top"

    # A private method for getting the data from given Endpoint
    def _get(self, item_type, params=None):
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        url = f"{self.base_url}/{item_type}"
        print(url)

        response = requests.get(url, headers=headers, params=params)

        return response
    

    def topItems(self, item, time_range = 'medium_term', limit=50):
        params = {
            "time_range": time_range,
            "limit": limit
        }
        response = self._get(f"{item}", params=params)

        if response.status_code != 200:
            print(response.content)
            return None
        
        json_data = response.json()
        return json_data.get("items", [])
    

    def topTracks(self, time_range, limit=50):

        json_data = self.topItems("tracks", time_range, limit)
        if json_data == None or []:
            return None
        
        all_tracks = []

        for item in json_data:
            track = {}
            track["song_name"] = item["name"]
            track["song_id"] = item["id"]
            track["song_url"] = item["external_urls"]["spotify"]
            track["song_image"] = settings.BASE_DIR/"resources/default.jpg" if item["album"]["images"] == [] else item["album"]["images"][-1]["url"]
            track["singer_names"] = [name["name"] for name in item["artists"]]

            all_tracks.append(track)
        
        print(settings.BASE_DIR/"resources/default.jpg")
        return all_tracks
    
    def topArtists(self, time_range, limit=50):

        json_data = self.topItems(item="artists", time_range=time_range, limit=limit)

        if json_data == None or []:
            return None


        all_artists = []

        for item in json_data:
            track = {}
            track["artist_name"] = item["name"]
            track["artist_id"] = item["id"]
            track["artist_genres"] = item["genres"]
            track["artist_url"] = item["external_urls"]["spotify"]
            track["artist_image"] = None if item["images"] == [] else item["images"][0]["url"]

            all_artists.append(track)
        
        return all_artists

    
    
        
      
    