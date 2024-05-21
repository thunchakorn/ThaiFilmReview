from rest_framework import serializers
from films.models import Film


class RoleSerializer(serializers.Serializer):
    name = serializers.StringRelatedField(source="person")
    role = serializers.CharField(max_length=100, source="name")


class FilmDetailSerializer(serializers.HyperlinkedModelSerializer):
    genres = serializers.StringRelatedField(many=True, read_only=True)
    directors = serializers.StringRelatedField(many=True, read_only=True)
    links = serializers.SlugRelatedField(many=True, read_only=True, slug_field="link")
    actors = RoleSerializer(many=True, source="role_set")
    average_rating = serializers.FloatField(source="avg_rating", read_only=True)

    class Meta:
        model = Film
        fields = (
            "name",
            "release_date",
            "genres",
            "directors",
            "actors",
            "links",
            "average_rating",
        )
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class FilmListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Film
        fields = (
            "url",
            "name",
        )
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}
