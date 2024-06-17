from django import forms
from django.db.models import F, OrderBy
import django_filters

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Film, Genre


class NullLastOrderingFilter(django_filters.OrderingFilter):
    def get_ordering_value(self, param):
        value = super().get_ordering_value(param)
        return OrderBy(
            F(value.lstrip("-")), descending=value.startswith("-"), nulls_last=True
        )


class FilmFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "grid grid-cols-2 grid-flow-row gap-x-2"
        self.helper.form_method = "get"
        self.helper.field_class = "mb-1"
        self.helper.label_class = "my-form-label block mb-1"

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
        label="ประเภท (กด Ctrl/⌘ + คลิก)",
        widget=forms.SelectMultiple,
    )

    order_by = NullLastOrderingFilter(
        fields=(("release_date", "release_date"),),
        field_labels={
            "release_date": "วันที่เข้าฉาย",
        },
        empty_label=None,
        choices=(
            ("-release_date", "วันที่เข้าฉาย ใหม่ไปเก่า"),
            ("release_date", "วันที่เข้าฉาย เก่าไปใหม่"),
            ("-reviews_count", "จำนวนรีวิว มากไปน้อย"),
            ("-average_rating", "คะแนนเฉลี่ย มากไปน้อย"),
        ),
        label="เรียงลำดับ",
    )
