from typing import Iterable
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import CustomUser

class ImageGroup(models.Model):
    name = models.CharField(max_length = 255)
    
    def __str__(self):
        return self.name

    
class UserImage(models.Model):
    image = models.ImageField(upload_to='images')
    original_image = models.ImageField(upload_to='images/original', null=True, blank=True)
    user = models.ForeignKey(CustomUser, models.CASCADE)
    group = models.ForeignKey(ImageGroup, models.CASCADE)
    title = models.CharField(max_length = 255)
    description = models.TextField()
    is_borderized = models.BooleanField(default=False)
    contrast_value = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(-100)])
    brightness_value = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(-100)])

    def __str__(self):
        return f'{self.title} ({self.user.username})' 
