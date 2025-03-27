from django.urls import path
from .views import ArtistListView, ArtistDetailView

urlpatterns = [
    path("", ArtistListView.as_view(), name="artist-list"),
    path(
        "<int:artist_id>/",
        ArtistDetailView.as_view(),
        name="artist-detail",
    ),
]
