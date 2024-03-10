from django.urls import include, path
from rest_framework import routers

from recipe.views import IngredientViewSet, TagViewSet

app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register('tags', TagViewSet, basename='Tag')
v1_router.register('ingredients', IngredientViewSet, basename='Ingredient')

urlpatterns = [
    path('', include(v1_router.urls)),
    path('', include('user.urls')),
]
