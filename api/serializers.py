from rest_framework import serializers

from api.models import UserImage, UserImageGroup


class UserImageSerializer(serializers.ModelSerializer):    
    class Meta:
        model = UserImage
        fields = '__all__'
        read_only_fields = ('id', 'group', 'user', 'original_image')

    def create(self, validated_data, group, user):
        validated_data['group'] = group
        validated_data['user'] = user
        validated_data['original_image'] = validated_data['image']
        return super().create(validated_data)
    
    def create_without_group(self, validated_data, user):
        validated_data['user'] = user
        validated_data['original_image'] = validated_data['image']
        return super().create(validated_data)


class UserImageUpdateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    title = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(required=False)
    
    class Meta:
        model = UserImage
        fields = ('image', 'title', 'description')

    def update(self, validated_data):
        for field, value in validated_data.items():
            setattr(self.instance, field, value)

        self.instance.save()
        return self.instance


class UserImageGroupSerializer(serializers.ModelSerializer):    
    class Meta:
        model = UserImageGroup
        fields = '__all__'
        read_only_fields = ('id', 'user')

    def create(self, validated_data, user):
        validated_data['user'] = user
        return super().create(validated_data)


    def update(self, validated_data):
        for field, value in validated_data.items():
            setattr(self.instance, field, value)

        return self.instance.save()