from rest_framework import viewsets

from . import serializers
from ..models import Film


class FilmViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Film.objects.with_reviews_data().all()
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.FilmDetailSerializer
        # else self.action == "retrieve"
        return serializers.FilmListSerializer
