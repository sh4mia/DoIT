from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default="default.png", null=True, blank=True)
    points = models.PositiveIntegerField(default=0)
    streak = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar:
            img = Image.open(self.avatar.path)
            img.thumbnail((500, 500))
            img.save(self.avatar.path)

    def level(self):
        if self.points >= 50:
            return 5
        elif self.points >= 20:
            return 4
        elif self.points >= 10:
            return 3
        elif self.points >= 5:
            return 2
        else:
            return 1