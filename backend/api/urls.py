from django.urls import include, path
from rest_framework import routers

from recipe.views import IngredientViewSet, RecipeViewSet, TagViewSet

app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register('tags', TagViewSet, basename='Tag')
v1_router.register('ingredients', IngredientViewSet, basename='Ingredient')
v1_router.register('recipes', RecipeViewSet, basename='Recipe')

urlpatterns = [
    path('', include(v1_router.urls)),
    path('', include('user.urls')),
]
