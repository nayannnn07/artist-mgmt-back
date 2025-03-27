from rest_framework import serializers

class MusicSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    artist_id = serializers.IntegerField()
    album_name = serializers.CharField(max_length=255, required=False)
    genre = serializers.ChoiceField(
        choices=[
            "rnb",
            "country",
            "classic",
            "rock",
            "jazz"  
            # "pop",
            # "hip-hop",
            # "blues",
            # "metal",
            # "ballad",
        ]
    )
    release_date = serializers.DateField(required=False)

    # # Get artist name from artist_id
    # def get_artist(self, obj):
    #     artist = ArtistModel.get_artist_by_id(obj.artist_id)  # Fetch artist details
    #     return artist[1] if artist else None  # Return artist name
