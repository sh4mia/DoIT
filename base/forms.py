from django import forms
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Reordering Form and View


class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        email = forms.EmailField()
        fields = ['username', 'email', 'password1', 'password2']

class PositionForm(forms.Form):
    position = forms.CharField()

class TaskForm(forms.ModelForm):
    due = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Task
        fields = ['title', 'description', 'complete', 'due']

