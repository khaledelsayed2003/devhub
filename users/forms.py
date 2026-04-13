from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill
from django.forms import ModelForm
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "email", "username", "password1", "password2"]
        labels = {
            "first_name": "Name",
        }


class ProfileForm(ModelForm):
    remove_profile_image = forms.BooleanField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Profile
        fields = [
            'name',
            'email',
            'username',
            'location',
            'bio',
            'short_intro',
            'profile_image',
            'social_github',
            'social_linkedin',
            'social_insta',
            'social_youtube',
            'social_website',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'How your name should appear publicly'}),
            'email': forms.EmailInput(attrs={'placeholder': 'name@example.com'}),
            'username': forms.TextInput(attrs={'placeholder': 'Your public username'}),
            'location': forms.TextInput(attrs={'placeholder': 'City, country or remote'}),
            'short_intro': forms.TextInput(attrs={'placeholder': 'A short one-line intro that quickly describes what you do'}),
            'bio': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Tell the story behind what you build, what you care about, and what people should know about your work.'}),
            'profile_image': forms.FileInput(attrs={'accept': 'image/*'}),
            'social_github': forms.URLInput(attrs={'placeholder': 'https://github.com/yourname'}),
            'social_linkedin': forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/yourname'}),
            'social_insta': forms.URLInput(attrs={'placeholder': 'https://instagram.com/yourname'}),
            'social_youtube': forms.URLInput(attrs={'placeholder': 'https://youtube.com/@yourchannel'}),
            'social_website': forms.URLInput(attrs={'placeholder': 'https://yourwebsite.com'}),
        }

    def save(self, commit=True):
        profile = super().save(commit=False)
        remove_profile_image = self.cleaned_data.get('remove_profile_image')
        image_field = Profile._meta.get_field('profile_image')
        default_image = image_field.default

        if remove_profile_image:
            current_image = getattr(profile, 'profile_image', None)
            if current_image and current_image.name and current_image.name != default_image:
                current_image.delete(save=False)
            profile.profile_image = default_image

        if commit:
            profile.save()

        return profile


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']