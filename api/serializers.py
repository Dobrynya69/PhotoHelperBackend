from rest_framework import serializers

from api.models import UserImage
from api.utils.user_image_utils import UserImageUtils

class UserImageSerializer(serializers.ModelSerializer):    
    class Meta:
        model = UserImage
        fields = '__all__'
        read_only_fields = ('id', 'user', 'is_borderized', 'original_image', 'contrast_value', 'brightness_value')
        
    def create(self, validated_data, user):
        validated_data['user'] = user
        validated_data['original_image'] = validated_data['image']
        user_image = super().create(validated_data)
        return user_image

class UserImageUpdateSerializer(serializers.ModelSerializer):    
    class Meta:
        model = UserImage
        fields = '__all__'
        read_only_fields = ('id', 'user', 'image', 'original_image')
        
    def update(self, instance, validated_data):
        user_image = super().update(instance, validated_data)
        user_image_utils = UserImageUtils(user_image, user_image.image.name.split("/")[-1])
        user_image_utils.update_user_image()
        return user_image

        