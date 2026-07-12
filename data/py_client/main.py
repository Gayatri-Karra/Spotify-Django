import requests
import os
from dotenv import load_dotenv
import base64
import json

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

token_url = 'https://accounts.spotify.com/api/token'



def get_token(code):

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': "http://localhost:8000/login",
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    response = requests.post(token_url, data=data)

    return response.json()


def get_userdata(access_token):
    """
    {'display_name': 'Anand', 'external_urls': {'spotify': 'https://open.spotify.com/user/ras0cidgbqdy4bv1g7tnx51rm'},
      'href': 'https://api.spotify.com/v1/users/ras0cidgbqdy4bv1g7tnx51rm', 
      'id': 'ras0cidgbqdy4bv1g7tnx51rm', 'images': [], 'type': 'user',
     'uri': 'spotify:user:ras0cidgbqdy4bv1g7tnx51rm', 'followers': {'href': None, 'total': 1},
     'country': 'IN', 'product': 'free', 'explicit_content': {'filter_enabled': False, 'filter_locked': False},
       'email': 'kshylaja777@gmail.com'}
    """

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    user_url = 'https://api.spotify.com/v1/me'
    user_reponse = requests.get(user_url, headers=headers)

    return user_reponse.json()


def token_refreshing(refresh_token):
    # token_url = 'https://accounts.spotify.com/api/token'

    data = {
    'grant_type': 'refresh_token',
    'refresh_token': refresh_token,
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET
    }

    response = requests.post(token_url, data=data)

    json_resp = response.json()
    newAccessToken = json_resp["access_token"]

    return newAccessToken



