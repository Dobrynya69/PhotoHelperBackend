from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action

from api.models import UserImage
from api.serializers import UserImageSerializer
from api.services.user_image_service import UserImageService

class UserImageViewSet(ModelViewSet):
    queryset = UserImage.objects.all()
    serializer_class = UserImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]


    @action(detail=True, methods=['post'])
    def create(self, request):
        service = UserImageService(request)
        return service.create()


    @action(detail=True, methods=['get'])
    def retrieve(self, request, pk):
        service = UserImageService(request)
        return service.get(pk)


    @action(detail=False, methods=['get'])
    def list(self, request, user_pk):
        service = UserImageService(request)
        return service.list(user_pk)


    @action(detail=True, methods=['delete'])
    def destroy(self, request, pk):
        service = UserImageService(request)
        return service.delete(pk)


    @action(detail=True, methods=['patch'])
    def partial_update(self, request, pk):
        service = UserImageService(request)
        return service.partial_update(pk)


    @action(detail=True, methods=['patch'])
    def borderize(self, request, user_pk):
        pass
