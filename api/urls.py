from django.urls import path
from api.views import UserImageViewSet, UserImageGroupViewSet


urlpatterns = [
    path('image/<user_image_pk>/group/<user_image_group_pk>/', UserImageViewSet.as_view({'put': 'group_update'})),
    path('image/group/<user_image_group_pk>/', UserImageViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('image/<user_image_pk>/borderized/', UserImageViewSet.as_view({'get': 'retrieve_borderized_image'})),
    path('image/<user_image_pk>/', UserImageViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('image/', UserImageViewSet.as_view({'post': 'create_without_group', 'get': 'list_without_group'})),

    path('group/<user_image_group_pk>/', UserImageGroupViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('group/', UserImageGroupViewSet.as_view({'get': 'list', 'post': 'create'})),
]
