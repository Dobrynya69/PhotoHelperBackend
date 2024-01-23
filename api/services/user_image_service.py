from rest_framework.response import Response
from rest_framework import status

from api.models import UserImage
from api.serializers import UserImageSerializer

class UserImageService():
    model_class = UserImage
    serializer_class = UserImageSerializer

    def __init__(self, request) -> None:
        self.request = request

    def create(self):
        user_image_serialized = self.serializer_class(data=self.request.data)
        user_image_serialized.initial_data['user'] = self.request.user.id
        if user_image_serialized.is_valid():
            user_image = user_image_serialized.create(user_image_serialized.validated_data)
            user_image_serialized.instance = user_image
            return Response(
                data=user_image_serialized.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            data=user_image_serialized.errors,
            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    def get(self, pk):
        try:
            user_image = self.model_class.objects.get(pk=pk)
        except self.model_class.DoesNotExist:
            return Response(
                data={'errors':{'Does not exists': 'User image with such id does not exists'}},
                status=status.HTTP_204_NO_CONTENT)

        user_image_serialized = self.serializer_class(instance=user_image)
        return Response(
            data=user_image_serialized.data,
            status=status.HTTP_200_OK)


    def delete(self, pk):
        try:
            user_image = self.model_class.objects.get(pk=pk)
        except self.model_class.DoesNotExist:
            return Response(
                data={'errors':{'Does not exists': 'User image with such id does not exists'}},
                status=status.HTTP_204_NO_CONTENT)

        user_image.delete()
        return Response(status=status.HTTP_200_OK)


    def partial_update(self, pk):
        try:
            user_image = self.model_class.objects.get(pk=pk)
        except self.model_class.DoesNotExist:
            return Response(
                data={'errors':{'Does not exists': 'User image with such id does not exists'}},
                status=status.HTTP_204_NO_CONTENT)

        user_image_serialized = self.serializer_class(user_image, data=self.request.data, partial=True)
        if user_image_serialized.is_valid():
            user_image_serialized.save()
            return Response(data=user_image_serialized.data, status=status.HTTP_200_OK)

        return Response(
            data=user_image_serialized.errors,
            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            


    def list(self, user_pk):
        user_image_serialized = self.serializer_class(self.model_class.objects.filter(user_id=user_pk), many=True)
        return Response(data=user_image_serialized.data, status=status.HTTP_201_CREATED)