from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated

from users.models import CustomUser
from users.serializers import UserSerializer
from users.services.user_service import UserService

class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'])
    def retrieve(self, request, pk):
        service = UserService(request)
        return service.get_by_pk(pk)

    @action(detail=True, methods=['post'])
    def create(self, request):
        service = UserService(request)
        return service.register()

    @action(detail=True, methods=['post'])
    def login(self, request):
        service = UserService(request)
        return service.login()

    @action(detail=True, methods=['delete'])
    @permission_classes([IsAuthenticated])
    def logout(self, request):
        service = UserService(request)
        return service.logout()
    
    @action(detail=True, methods=['get'])
    @permission_classes([IsAuthenticated])
    def get_current_user(self, request):
        service = UserService(request)
        return service.get_current_user()