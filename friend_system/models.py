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

    def get_rank_name(self):
        if self.points >= 750:
            return "Master"
        elif self.points >= 250:
            return "Expert"
        elif self.points >= 100:
            return "Intermediate"
        elif self.points >= 50:
            return "Beginner"
        else:
            return "Newbie"
        