from django import forms

from .models import Profile

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field


# Create the form class.
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "profile_pic",
            "name",
            "bio",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.label_class = "my-form-label block mb-1"
        self.helper.layout = Layout(
            Field("profile_pic", css_class="file-input"),
            "name",
            "bio",
            Submit("submit", "Submit", css_class="btn-sm"),
        )

    name = forms.CharField(max_length=100, label="ชื่อที่แสดง")
    bio = forms.CharField(max_length=1000, label="เกี่ยวกับฉัน")
    profile_pic = forms.ImageField(label="รูปโปรไฟล์")
