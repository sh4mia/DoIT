from django import forms
from .models import Task

# Reordering Form and View


class PositionForm(forms.Form):
    position = forms.CharField()

class TaskForm(forms.ModelForm):
    due = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Task
        fields = ['title', 'description', 'complete', 'due']

