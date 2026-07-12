import requests
import json


def all_playlists(access_token):

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    url = "https://api.spotify.com/v1/me/playlists"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(response.content)
        return None
    json_data = response.json()

    playlists = []
    for item in json_data["items"]:
        single = {}

        single["playlist_name"] = item["name"]
        single["playlist_image"] = item["images"][0]["url"] if item["images"] else None
        single["playlist_url"] = item["external_urls"]["spotify"]
        single["playlist_owner"] = item["owner"]["display_name"]

        playlists.append(single)

    return playlists


def create_playlist(access_token, user_id, name, description, is_public: bool):

    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    data = {
        "name": name,
        "description": description,
        "public": is_public
    }
    data = json.dumps(data)
    response = requests.post(url, headers=headers, data=data)

    print(response.content)


