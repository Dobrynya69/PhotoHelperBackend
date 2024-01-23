from django.urls import path
from users.views.user_views import UserViewSet

urlpatterns = [
    path('', UserViewSet.as_view({'post': 'create', 'get': 'get_current_user', 'delete': 'logout'})),
    path('login', UserViewSet.as_view({'post': 'login'})),
    path('<pk>', UserViewSet.as_view({'get': 'retrieve'})),
]
