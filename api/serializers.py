from rest_framework import serializers

from api.models import UserImage

class UserImageSerializer(serializers.ModelSerializer):    
    class Meta:
        model = UserImage
        fields = '__all__'
