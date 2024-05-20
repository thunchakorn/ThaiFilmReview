from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Field

from .models import Review


class StarRatingWidget(forms.widgets.ChoiceWidget):
    template_name = "widgets/star_rating.html"

    def __init__(self, attrs=None, choices=()):
        super().__init__(attrs, choices)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ["profile", "film"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.field_class = "mb-1"
        self.helper.label_class = "my-form-label block mb-1"

        self.helper.layout = Layout(
            Fieldset(
                "คะแนน",
                "rating",
                "screenplay_rating",
                "acting_rating",
                "production_rating",
                "cinematography_rating",
                "sound_rating",
                css_class="grid grid-cols-2 grid-flow-row gap-x-2",
            ),
            Fieldset(
                "เขียนรีวิว",
                "short_review",
                "is_spoiler",
                "full_review",
            ),
        )
        self.helper.add_input(Submit("submit", "Submit", css_class="btn-sm"))

    RATING_CHOICES = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]

    rating = forms.TypedChoiceField(
        choices=RATING_CHOICES,
        required=True,
        label="ภาพรวม",
        coerce=int,
        widget=StarRatingWidget,
    )
    screenplay_rating = forms.TypedChoiceField(
        choices=RATING_CHOICES,
        required=True,
        label="ด้านงานบท",
        coerce=int,
        widget=StarRatingWidget,
    )
    acting_rating = forms.TypedChoiceField(
        choices=RATING_CHOICES,
        required=True,
        label="ด้านงานแสดง",
        coerce=int,
        widget=StarRatingWidget,
    )
    production_rating = forms.TypedChoiceField(
        choices=RATING_CHOICES,
        required=True,
        label="ด้านงานสร้าง",
        coerce=int,
        widget=StarRatingWidget,
    )
    cinematography_rating = forms.TypedChoiceField(
        choices=RATING_CHOICES,
        required=True,
        label="ด้านงานภาพ",
        coerce=int,
        widget=StarRatingWidget,
    )
    sound_rating = forms.TypedChoiceField(
        choices=RATING_CHOICES,
        required=True,
        label="ด้านงานเสียง",
        coerce=int,
        widget=StarRatingWidget,
    )

    is_spoiler = forms.BooleanField(label="รีวิวเต็มมีสปอยล์หรือไม่", required=False)
    is_spoiler.widget.attrs["class"] = "checkbox"

    short_review = forms.CharField(max_length=64, label="รีวิวย่อ (ห้ามสปอยล์)")
    full_review = forms.CharField(
        max_length=12000, label="รีวิวเต็ม", widget=forms.Textarea
    )
