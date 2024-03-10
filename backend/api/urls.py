from django.urls import include, path
from rest_framework import routers

from recipe.views import TagViewSet

app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register('tags', TagViewSet, basename='Tag')

urlpatterns = [
    path('', include(v1_router.urls)),
    path('', include('user.urls')),
]
