from django import forms
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Reordering Form and View


class CustomUserForm(forms.Form):

    username = forms.CharField(max_length=255, label= 'Username:')
    email = forms.EmailField(max_length=255, label= 'E-mail:')
    password1 = forms.CharField(max_length=128, widget=forms.PasswordInput, label= 'Password:')
    password2 = forms.CharField(max_length=128, widget=forms.PasswordInput, label= 'Repeat Password:')

    def clean_email(self):
        email = self.cleaned_data['email']
        users = User.objects.filter(email=email)
        if users:
            raise forms.ValidationError('Email is already in use.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists.')
        if len(username) < 3:
            raise forms.ValidationError('Username must be at least 3 characters long.')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        if password1 is None:
            raise forms.ValidationError('Please enter a password.')
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        return password2

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data
    
    def save(self, commit=True):
        user = User(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
        )
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class PositionForm(forms.Form):
    position = forms.CharField()

class TaskForm(forms.ModelForm):
    due = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Task
        fields = ['title', 'description', 'complete', 'due']

