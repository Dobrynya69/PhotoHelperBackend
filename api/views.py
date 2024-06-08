from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status

from django.http import HttpResponse
from django.db import IntegrityError

from PIL import Image

from project.utils import Utils
from api.utils import UserImageUtils
from api.models import UserImage, UserImageGroup
from api.serializers import UserImageSerializer, UserImageUpdateSerializer, UserImageGroupSerializer
from api.permissions import IsAuthorSafe


class UserImageViewSet(GenericViewSet):
    queryset=UserImage.objects.all()
    serializer_class=UserImageSerializer
    permission_classes=[IsAuthorSafe]

    def get_object(self):
        response_object = UserImage.objects.get(pk=self.kwargs['user_image_pk'])
        self.check_object_permissions(self.request, response_object)
        return response_object


    def get_group_object(self):
        response_object = UserImageGroup.objects.get(pk=self.kwargs['user_image_group_pk'])
        self.check_object_permissions(self.request, response_object)
        return response_object


    def retrieve(self, request, *args, **kwargs):
        try:
            response_object = self.get_object()
        except UserImage.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        response_serializer = UserImageSerializer(instance=response_object)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


    def retrieve_borderized_image(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except UserImage.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        request_image = Image.open(instance.image)
        request_color = request.GET.get('color', 'white')

        response_image = UserImageUtils.borderize_image(request_image, request_color)
        response = HttpResponse(content_type=f'image/{response_image.format.lower()}')
        response_image.save(response, response_image.format.capitalize())
        return response


    def group_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except UserImage.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        try:
            group_object = self.get_group_object()
        except UserImageGroup.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        instance.group = group_object
        instance.save()

        response_serializer = UserImageSerializer(instance=instance)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


    def list(self, request, *args, **kwargs):
        try:
            group_object = self.get_group_object()
        except UserImageGroup.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        try:
            response_objects = UserImage.objects.filter(group=group_object).all().order_by("title")
        except UserImage.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        response_serializer = UserImageSerializer(instance=response_objects, many=True)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


    def list_without_group(self, request, *args, **kwargs):
        try:
            user_object = request.user
            response_objects = UserImage.objects.filter(user=user_object, group=None).all().order_by("title")
        except UserImage.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        response_serializer = UserImageSerializer(instance=response_objects, many=True)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        request_serializer = UserImageSerializer(data=request.data)
        if request_serializer.is_valid():
            try:
                group_object = self.get_group_object()
            except UserImageGroup.DoesNotExist:
                return Response(status=status.HTTP_204_NO_CONTENT)

            user_object = request.user
            response_object = request_serializer.create(request_serializer.validated_data, group_object, user_object)
            response_serializer = UserImageSerializer(instance=response_object)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {'error': Utils.serializer_errors_to_string(request_serializer.errors)},
            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


    def create_without_group(self, request, *args, **kwargs):
        request_serializer = UserImageSerializer(data=request.data)
        if request_serializer.is_valid():
            user_object = request.user
            response_object = request_serializer.create_without_group(request_serializer.validated_data, user_object)
            response_serializer = UserImageSerializer(instance=response_object)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {'error': Utils.serializer_errors_to_string(request_serializer.errors)},
            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except UserImage.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        request_serializer = UserImageUpdateSerializer(instance=instance, data=request.data)
        if request_serializer.is_valid():
            response_object = request_serializer.update(request_serializer.validated_data)
            response_serializer = UserImageSerializer(instance=response_object)
            return Response(response_serializer.data, status=status.HTTP_200_OK)

        return Response(
            {'error': Utils.serializer_errors_to_string(request_serializer.errors)},
            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


    def group_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except UserImage.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        try:
            group_object = self.get_group_object()
        except UserImageGroup.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        instance.group = group_object
        instance.save()

        response_serializer = UserImageSerializer(instance=instance)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except UserImage.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        instance.delete()
        return Response(status=status.HTTP_200_OK)


class UserImageGroupViewSet(GenericViewSet):
    queryset=UserImageGroup.objects.all()
    serializer_class=UserImageGroupSerializer
    permission_classes=[IsAuthorSafe]

    def get_object(self):
        response_object = UserImageGroup.objects.get(pk=self.kwargs['user_image_group_pk'])
        self.check_object_permissions(self.request, response_object)
        return response_object


    def retrieve(self, request, *args, **kwargs):
        try:
            response_object = self.get_object()
        except UserImageGroup.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        response_serializer = UserImageGroupSerializer(instance=response_object)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


    def list(self, request, *args, **kwargs):
        user_object = request.user

        try:
            response_objects = UserImageGroup.objects.filter(user=user_object).all().order_by('name')
        except UserImageGroup.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        response_serializer = UserImageGroupSerializer(instance=response_objects, many=True)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        request_serializer = UserImageGroupSerializer(data=request.data)
        if request_serializer.is_valid():
            user_object = request.user
            try:
                response_object = request_serializer.create(request_serializer.validated_data, user_object)
            except IntegrityError:
                return Response(
                    {'error': f'Group "{request_serializer.initial_data["name"]}" already exists.'},
                    status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

            response_serializer = UserImageGroupSerializer(instance=response_object)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {'error': Utils.serializer_errors_to_string(request_serializer.errors)},
            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except UserImageGroup.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        request_serializer = UserImageGroupSerializer(instance=instance, data=request.data)
        if request_serializer.is_valid():
            try:
                response_object = request_serializer.update(request_serializer.validated_data)
            except IntegrityError:
                return Response(
                    {'error': f'Group "{request_serializer.initial_data["name"]}" already exists.'},
                    status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            response_serializer = UserImageGroupSerializer(instance=response_object)
            return Response(response_serializer.data, status=status.HTTP_200_OK)

        return Response(
            {'error': Utils.serializer_errors_to_string(request_serializer.errors)},
            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except UserImageGroup.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        instance.delete()
        return Response(status=status.HTTP_200_OK)