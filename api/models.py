from django.db import models

from users.models import CustomUser


class UserImageGroup(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, models.CASCADE)

    class Meta:
        unique_together = ('name', 'user')

    def __str__(self):
        return self.name


class UserImage(models.Model):
    image = models.ImageField(upload_to='images')
    original_image = models.ImageField(upload_to='images/original', null=True, blank=True)
    user = models.ForeignKey(CustomUser, models.CASCADE)
    group = models.ForeignKey(UserImageGroup, models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.title} ({self.user.username})' 
