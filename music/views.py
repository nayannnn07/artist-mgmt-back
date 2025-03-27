from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MusicModel
from .serializers import MusicSerializer


class MusicListView(APIView):
    def get(self, request):
        """Retrieve all music records along with artist names."""
        music_list = MusicModel.get_all_music()
        if music_list:
            music_data = [
                {
                    "id": music[0],
                    "title": music[1],
                    "artist": music[2],  # Fetching artist name instead of ID
                    "album_name": music[3],
                    "genre": music[4],
                    "created_at": music[5],
                    "updated_at": music[6],
                }
                for music in music_list
            ]
            return Response(music_data, status=status.HTTP_200_OK)
        return Response({"message": "No music found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """Create a new music record."""
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            music_id = MusicModel.create_music(
                data["title"], data["artist_id"], data.get("album_name"), data["genre"]
            )
            return Response(
                {"message": "Music created successfully", "music_id": music_id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MusicDetailView(APIView):
    def get(self, request, music_id):
        """Retrieve a single music record by ID along with artist name."""
        music = MusicModel.get_music_by_id(music_id)
        if music:
            music_data = {
                "id": music[0],
                "title": music[1],
                "artist": music[2],  # Fetching artist name instead of ID
                "album_name": music[3],
                "genre": music[4],
                "created_at": music[5],
                "updated_at": music[6],
            }
            return Response(music_data, status=status.HTTP_200_OK)
        return Response({"error": "Music not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, music_id):
        """Update a music record."""
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            updated = MusicModel.update_music(
                music_id,
                data["title"],
                data["artist_id"],
                data.get("album_name"),
                data["genre"],
            )
            if updated:
                return Response(
                    {"message": "Music updated successfully"}, status=status.HTTP_200_OK
                )
            return Response(
                {"error": "Music not found"}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, music_id):
        """Delete a music record."""
        deleted = MusicModel.delete_music(music_id)
        if deleted:
            return Response(
                {"message": "Music deleted successfully"}, status=status.HTTP_200_OK
            )
        return Response({"error": "Music not found"}, status=status.HTTP_404_NOT_FOUND)
