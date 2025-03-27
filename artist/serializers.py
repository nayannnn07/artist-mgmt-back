from rest_framework import serializers


class ArtistSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    dob = serializers.DateTimeField()
    gender = serializers.ChoiceField(choices=["m", "f", "o"])
    address = serializers.CharField(max_length=255)
    first_release_year = serializers.DateField()
    no_of_albums_released = serializers.IntegerField()
