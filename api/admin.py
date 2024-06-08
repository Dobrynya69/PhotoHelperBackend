from django.contrib import admin

from api.models import UserImage, UserImageGroup


admin.site.register(UserImageGroup)
admin.site.register(UserImage)
