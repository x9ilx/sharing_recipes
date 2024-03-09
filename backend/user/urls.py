from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FoodgramUserViewSet

user_router = DefaultRouter()
user_router.register('users', FoodgramUserViewSet)

app_name = 'user'

urlpatterns = [
    # path('', include('djoser.urls')),
    path('', include(user_router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
