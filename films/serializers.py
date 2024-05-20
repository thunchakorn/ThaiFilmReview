from rest_framework import serializers
from films.models import Film


class RoleSerializer(serializers.Serializer):
    actor = serializers.StringRelatedField(source="person")
    role = serializers.CharField(max_length=100, source="name")


class FilmSerializer(serializers.ModelSerializer):
    genres = serializers.StringRelatedField(many=True, read_only=True)
    directors = serializers.StringRelatedField(many=True, read_only=True)
    links = serializers.SlugRelatedField(many=True, read_only=True, slug_field="link")
    role_set = RoleSerializer(many=True)

    class Meta:
        model = Film
        fields = ["name", "release_date", "genres", "directors", "role_set", "links"]
