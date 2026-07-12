from django.shortcuts import render, redirect, HttpResponse
from django.core.cache import cache

import requests
import json
from dotenv import load_dotenv
from os import getenv

from .py_client import main, top_items, playlists, recommend
from .py_client.top_items import TopItems

# Create your views here.

load_dotenv()

CLIENT_ID = getenv("CLIENT_ID")
CLIENT_SECRET = getenv("CLIENT_SECRET")


def login_check(func):
    def wrapper(request, *args, **kwargs):
        if 'name' in request.session:
            print("oh nooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
            return func(request, *args, **kwargs)
        else:
            return redirect('login')
    
    return wrapper


def login_view(request):

    code = request.GET.get('code')

    if code == None:
        """Spotify login will return a code which can be used to
         get refresh and access token for the user"""
        return redirect(f'https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri=http://localhost:8000/login&scope=user-read-private%20user-read-email%20user-top-read%20user-read-recently-played%20user-read-playback-position%20user-read-playback-state%20user-modify-playback-state%20user-read-currently-playing%20playlist-read-private%20playlist-read-collaborative%20playlist-modify-private%20playlist-modify-public%20user-follow-modify%20user-follow-read%20user-library-modify%20user-library-read')

    token_data = main.get_token(code)


    request.session['refresh_token'] = token_data["refresh_token"]
    request.session['access_token'] = token_data["access_token"]


    user_data = main.get_userdata(token_data["access_token"])
    # print(user_data, '--------------------------------------------------------------')
    request.session['name'] = user_data["display_name"]
    request.session['user_id'] = user_data["id"]

    return redirect('home')



def get_token(request):
    refresh_token = request.session['refresh_token']
    newAccessToken = main.token_refreshing(refresh_token)

    request.session['access_token'] = newAccessToken
    

@login_check
def homepage_view(request):
    context = {
        'name': request.session['name']
    }
    return render(request, 'data/homepage.html', context)


@login_check
def top_tracks_view(request):
    access_token = request.session['access_token']
    time_range = request.GET.get('time_range') or "medium_term"

    all_tracks = cache.get(f"{time_range}_tracks")

    if all_tracks == None:
        all_tracks = TopItems(access_token).topTracks(time_range=time_range)

        if all_tracks == None:
            get_token(request)
            return HttpResponse("Token Refersed, Please refresh the page.")
            
        print(f"Canching tracks {time_range}.....")
        cache.set(f"{time_range}_tracks", all_tracks, 3600)
    

    context = {
        "all_tracks": all_tracks
    }

    return render(request, 'data/top_tracks.html', context)


@login_check
def top_artists_view(request):
    access_token = request.session['access_token']
    time_range = request.GET.get('time_range') or 'medium_term'

    all_artists = cache.get(f"{time_range}_artists")

    if all_artists == None:

        all_artists = TopItems(access_token).topArtists(time_range=time_range)

        if all_artists == None:
            get_token(request)
            return HttpResponse("Token Refersed, Please refresh the page.")
            

        print(f"Caching Artists {time_range}......")
        cache.set(f"{time_range}_artists", all_artists, 3600)

    context = {
        "all_artists": all_artists
    }

    return render(request, 'data/top_artists.html', context)


@login_check
def playlists_view(request):
    access_token = request.session["access_token"]
    user_id = request.session["user_id"]

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        is_public = True if request.POST.get('is_public') == 'on' else False
        # print(name, description, is_public)
        playlists.create_playlist(access_token, user_id, name, description, is_public)

    all_playlists = playlists.all_playlists(access_token)
    if all_playlists == None:
        get_token(request)
        return HttpResponse("Token Refersed, Please refresh the page.")

    context = {
        "all_playlists": all_playlists
    }
    return render(request, 'data/playlist.html', context)


@login_check
def trackRecommendations_view(request):
    access_token = request.session['access_token']

    recommendations = recommend.track_recommend(access_token)

    context = {
        "short_term": recommendations["short_term"],
        "medium_term": recommendations["medium_term"],
        "long_term": recommendations["long_term"],
    }
    return render(request, "data/recommend.html", context)