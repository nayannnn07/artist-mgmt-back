from django.urls import path
from .views import MusicListView, MusicDetailView

urlpatterns = [
    path("", MusicListView.as_view(), name="music-list"),
    path("<int:music_id>/", MusicDetailView.as_view(), name="music-detail"),
]
