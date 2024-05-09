from django.forms import ModelForm
from profiles.models import Profile


# Create the form class.
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            "bio",
            "profile_pic",
        ]
