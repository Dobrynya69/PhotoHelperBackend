from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate

from users.models import CustomUser
from users.serializers import UserSerializer, UserLoginSerializer

class UserService():
    model_class = CustomUser
    serializer_class = UserSerializer
    login_serializer_class = UserLoginSerializer


    def __init__(self, request) -> None:
        self.request = request


    def get_by_pk(self, pk):
        try:
            user = self.model_class.objects.get(pk=pk)
        except self.model_class.DoesNotExist:
            return Response(
                data={'errors':{'Does not exists': 'User with such username does not exists'}},
                status=status.HTTP_204_NO_CONTENT)

        user_serialized = self.serializer_class(instance=user)
        return Response(
            data=user_serialized.data,
            status=status.HTTP_200_OK)


    def register(self):
        user_serialized = self.serializer_class(data=self.request.data)
        if user_serialized.is_valid():
            user = user_serialized.create(user_serialized.validated_data)
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                data={"user_pk": user.pk, "user_token": token.key},
                status=status.HTTP_201_CREATED
            )

        return Response(
            data=user_serialized.errors,
            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


    def login(self):
        login_serialized = self.login_serializer_class(data=self.request.data)
        if login_serialized.is_valid():
            user = authenticate(username=login_serialized.data.get('username'),
                                password=login_serialized.data.get('password'))
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                data={"user_pk": user.pk, "user_token": token.key},
                status=status.HTTP_200_OK
            )

        return Response(
            data=login_serialized.errors,
            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


    def logout(self):
        user = self.request.user
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            return Response(
                data={'errors':{'Does not exists': 'Token does not exists'}},
                status=status.HTTP_200_OK)

        token.delete()
        return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


    def get_current_user(self):
        user = self.request.user
        user_serialized = self.serializer_class(instance=user)
        return Response(data=user_serialized.data, status=status.HTTP_200_OK)
