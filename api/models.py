from django.db import models

from users.models import CustomUser

class ImageGroup(models.Model):
    name = models.CharField(max_length = 255)
    
    def __str__(self):
        return self.name

    
class UserImage(models.Model):
    image = models.ImageField(upload_to='images')
    user = models.ForeignKey(CustomUser, models.CASCADE)
    group = models.ForeignKey(ImageGroup, models.CASCADE)
    title = models.CharField(max_length = 255)
    description = models.TextField()
    is_borderized = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} ({self.user.username})' 
