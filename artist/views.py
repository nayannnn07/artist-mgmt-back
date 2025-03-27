from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ArtistModel
from .serializers import ArtistSerializer


class ArtistListView(APIView):
    def get(self, request):
        """Retrieve all artist records."""
        artists = ArtistModel.get_all_artists()
        if artists:
            artist_list = [
                {
                    "id": artist[0],
                    "name": artist[1],
                    "dob": artist[2],
                    "gender": artist[3],
                    "address": artist[4],
                    "first_release_year": artist[5],
                    "no_of_albums_released": artist[6],
                    "created_at": artist[7],
                    "updated_at": artist[8],
                }
                for artist in artists
            ]
            return Response(artist_list, status=status.HTTP_200_OK)
        return Response(
            {"message": "No artists found"}, status=status.HTTP_404_NOT_FOUND
        )

    def post(self, request):
        """Create a new artist record."""
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            artist_id = ArtistModel.create_artist(
                data["name"],
                data["dob"],
                data["gender"],
                data["address"],
                data["first_release_year"],
                data["no_of_albums_released"],
            )
            return Response(
                {"message": "Artist created successfully", "artist_id": artist_id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArtistDetailView(APIView):
    def get(self, request, artist_id):
        """Retrieve a single artist record by ID."""
        artist = ArtistModel.get_artist_by_id(artist_id)
        if artist:
            artist_data = {
                "id": artist[0],
                "name": artist[1],
                "dob": artist[2],
                "gender": artist[3],
                "address": artist[4],
                "first_release_year": artist[5],
                "no_of_albums_released": artist[6],
                "created_at": artist[7],
                "updated_at": artist[8],
            }
            return Response(artist_data, status=status.HTTP_200_OK)
        return Response({"error": "Artist not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, artist_id):
        """Update an artist record."""
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            updated = ArtistModel.update_artist(
                artist_id,
                data["name"],
                data["dob"],
                data["gender"],
                data["address"],
                data["first_release_year"],
                data["no_of_albums_released"],
            )
            if updated:
                return Response(
                    {"message": "Artist updated successfully"},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": "Artist not found"}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, artist_id):
        """Delete an artist record."""
        deleted = ArtistModel.delete_artist(artist_id)
        if deleted:
            return Response(
                {"message": "Artist deleted successfully"}, status=status.HTTP_200_OK
            )
        return Response({"error": "Artist not found"}, status=status.HTTP_404_NOT_FOUND)
