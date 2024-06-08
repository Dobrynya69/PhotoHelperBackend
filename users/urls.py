from django.urls import path
from users.views import UserViewSet


urlpatterns = [
    path('', UserViewSet.as_view({'post': 'create', 'get': 'retrieve_current', 'delete': 'logout', 'patch': 'partial_update'})),
    path('login/', UserViewSet.as_view({'post': 'login'})),
    path('<pk>/', UserViewSet.as_view({'get': 'retrieve'})),
]
