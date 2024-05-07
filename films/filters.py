import django_filters
from films.models import Film

class FilmFilter(django_filters.FilterSet):
    class Meta:
        model = Film
        fields = {
            'name': ['icontains'],
            'release_date': ['year__exact'],
            # 'genres__name': ['year__exact'],
        }
    o = django_filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('release_date', 'release_date'),
        ),

        # labels do not need to retain order
        field_labels={
            'release_date': 'วันที่เข้าฉาย',
        },

        choices=(
            ('-release_date', 'วันที่เข้าฉาย ใหม่ไปเก่า'),
            ('release_date', 'วันที่เข้าฉาย เก่าไปใหม่'),
        )
    )