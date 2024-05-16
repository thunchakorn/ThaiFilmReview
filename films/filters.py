import django_filters
from films.models import Film, Genre

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class FilmFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "grid grid-cols-2 grid-flow-row gap-x-2"
        self.helper.form_method = "get"

        self.helper.add_input(Submit("submit", "Submit", css_class="btn-sm"))


class FilmFilter(django_filters.FilterSet):
    class Meta:
        model = Film
        fields = ["name", "release_date", "genres"]
        form = FilmFilterForm

    name = django_filters.CharFilter("name", lookup_expr="icontains", label="ชื่อหนัง")
    release_date = django_filters.NumberFilter(
        "release_date", lookup_expr="year__exact", label="ปีที่เข้าฉาย"
    )

    def get_genres(request):
        return Genre.objects.all()

    genres = django_filters.ModelMultipleChoiceFilter(
        queryset=get_genres,
        label="ประเภท",
        # empty_label=None,
        widget=forms.SelectMultiple,
    )

    o = django_filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(("release_date", "release_date"),),
        # labels do not need to retain order
        field_labels={
            "release_date": "วันที่เข้าฉาย",
        },
        empty_label=None,
        choices=(
            ("-release_date", "วันที่เข้าฉาย ใหม่ไปเก่า"),
            ("release_date", "วันที่เข้าฉาย เก่าไปใหม่"),
        ),
        label="เรียงลำดับ",
    )
