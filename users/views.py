from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.contrib.auth import authenticate

from project.utils import Utils
from users.models import CustomUser
from users.serializers import UserSerializer, UserUpdateSerializer, UserLoginSerializer


class UserViewSet(GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'create', 'login']:
            self.permission_classes = (AllowAny, )
        elif self.action in ['retrieve_current', 'partial_update', 'logout']:
            self.permission_classes = (IsAuthenticated, )

        return super().get_permissions()


    def retrieve(self, request, *args, **kwargs):
        try:
            response_object = self.get_object()
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        response_serializer = UserSerializer(instance=response_object)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


    def retrieve_current(self, request):
        response_object = request.user
        response_serializer = UserSerializer(instance=response_object)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        request_serializer = UserSerializer(data=request.data)
        if request_serializer.is_valid():
            response_object = request_serializer.create(request_serializer.validated_data)
            response_serializer = UserSerializer(instance=response_object)
            token, _ = Token.objects.get_or_create(user=response_object)
            return Response({'token': token.key, 'user': response_serializer.data}, status=status.HTTP_201_CREATED)

        return Response(
            {'error': Utils.serializer_errors_to_string(request_serializer.errors)},
            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


    def partial_update(self, request, *args, **kwargs):
        instance = request.user
        request_serializer = UserUpdateSerializer(instance=instance, data=request.data)
        if request_serializer.is_valid():
            response_object = request_serializer.update(request_serializer.validated_data)
            response_serializer = UserSerializer(instance=response_object)
            return Response(response_serializer.data, status=status.HTTP_200_OK)

        return Response(
            {'error': Utils.serializer_errors_to_string(request_serializer.errors)},
            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


    def login(self, request, *args, **kwargs):
        request_serializer = UserLoginSerializer(data=request.data)
        if request_serializer.is_valid():
            response_object = authenticate(username=request_serializer.data.get('username'),
                                password=request_serializer.data.get('password'))
            if response_object is not None:
                response_serializer = UserSerializer(instance=response_object)
                token, _ = Token.objects.get_or_create(user=response_object)
                return Response(data={'token': token.key, 'user': response_serializer.data}, status=status.HTTP_200_OK)

            return Response({'error': 'Invalid credentials'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        return Response(
            {'error': Utils.serializer_errors_to_string(request_serializer.errors)},
            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


    def logout(self, request, *args, **kwargs):
        instance = request.user
        try:
            Token.objects.get(user=instance).delete()
        except Token.DoesNotExist:
            return Response({'error': 'Token does not exists'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        else:
            return Response(status=status.HTTP_200_OK)