from rest_framework import viewsets
from films import serializers
from django.db.models import Avg

from films.models import Film


class FilmViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Film.objects.all().annotate(avg_rating=Avg("reviews__overall_rating"))
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.FilmDetailSerializer
        return serializers.FilmListSerializer
