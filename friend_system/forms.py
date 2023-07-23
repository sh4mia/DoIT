from django import forms
from .models import UserProfile

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput, label='E-mail:', required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    class Meta:
        model = UserProfile
        fields = ['email', 'first_name', 'last_name']