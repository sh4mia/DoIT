from django import forms
from .models import UserProfile
from django.contrib.auth.models import User

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)
    class Meta:
        model = UserProfile
        fields = ['avatar']
    avatar = forms.ImageField(widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}),help_text='Acceptable File format: PNG only')