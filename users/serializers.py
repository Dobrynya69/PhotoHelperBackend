from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    avatar = serializers.ImageField(allow_null=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'avatar', 'password']
        read_only_fields = ['id']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'avatar']

    def update(self, validated_data):
        for field, value in validated_data.items():
            setattr(self.instance, field, value)

        self.instance.save()
        return self.instance


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
