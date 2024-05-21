from django.urls import path
from api.views.user_image_views import UserImageViewSet

urlpatterns = [
    path('image/', UserImageViewSet.as_view({'post': 'create'})),
    path('image/<pk>', UserImageViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('image/list/<user_pk>', UserImageViewSet.as_view({'get': 'list'})),
]
