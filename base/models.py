from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    due = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')

    def __str__(self):
        return self.title
    
    class Meta:
        order_with_respect_to = 'user'


