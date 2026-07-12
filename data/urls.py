from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage_view, name="home"),
    path('login/', views.login_view, name="login"),
    path('top-tracks/', views.top_tracks_view, name="top-tracks"),
    path('top-artists/', views.top_artists_view, name="top-artists"),
    path('playlists/', views.playlists_view, name="playlists"),
    path('recommend/', views.trackRecommendations_view, name='track-recommend')


    # path('set/', views.set_cookie),
    # path('get/', views.get_cookie),
]