from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default="default.png", null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar:
            img = Image.open(self.avatar.path)
            img.thumbnail((500, 500))
            img.save(self.avatar.path)